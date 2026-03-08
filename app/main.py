"""
FitBuddy — AI Fitness Plan Generator
FastAPI backend. API key lives in .env. Users never see it.
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.config import APP_TITLE, APP_VERSION
from app.db import init_db, get_db, UserPlan
from app import ai


# ─── LIFESPAN ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# ─── APP SETUP ───────────────────────────────────────────────────────────────

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="AI-powered fitness plan generator using Google Gemini",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def _profile_summary(plan: UserPlan) -> str:
    return (
        f"{plan.name}, {plan.age}yo {plan.gender}, "
        f"{plan.weight}kg/{plan.height}cm, Goal: {plan.goal}, "
        f"Level: {plan.fitness_level}, Intensity: {plan.workout_intensity}"
    )


# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    goal: str = Form(...),
    fitness_level: str = Form(...),
    workout_intensity: str = Form("Moderate"),
    days_per_week: int = Form(...),
    workout_duration: int = Form(...),
    equipment: str = Form(...),
    dietary_pref: str = Form(...),
    allergies: str = Form("None"),
    activity_level: str = Form(...),
    limitations: str = Form("None"),
    db: AsyncSession = Depends(get_db),
):
    # Build a lightweight profile object for AI functions
    class Profile:
        pass

    profile = Profile()
    profile.name = name.strip()
    profile.age = age
    profile.gender = gender
    profile.weight = weight
    profile.height = height
    profile.goal = goal
    profile.fitness_level = fitness_level
    profile.workout_intensity = workout_intensity
    profile.days_per_week = days_per_week
    profile.workout_duration = workout_duration
    profile.equipment = equipment
    profile.dietary_pref = dietary_pref
    profile.allergies = allergies or "None"
    profile.activity_level = activity_level
    profile.limitations = limitations or "None"
    profile.bmi = round(weight / ((height / 100) ** 2), 1)

    # ─── High-Availability Cache Layer ───
    # Check if an identical plan was generated recently (last 24h) to save quota
    from sqlalchemy import and_
    from datetime import timedelta
    
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    stmt = select(UserPlan).where(
        and_(
            UserPlan.goal == goal,
            UserPlan.age == age,
            UserPlan.fitness_level == fitness_level,
            UserPlan.workout_intensity == workout_intensity,
            UserPlan.weight == weight,
            UserPlan.created_at >= recent_cutoff
        )
    ).order_by(desc(UserPlan.created_at)).limit(1)
    
    cache_result = await db.execute(stmt)
    existing_plan = cache_result.scalars().first()
    
    if existing_plan:
        # Clone for the new user name but keep AI content
        record = UserPlan(
            name=name.strip(), age=age, gender=gender,
            weight=weight, height=height, goal=goal,
            fitness_level=fitness_level, workout_intensity=workout_intensity, days_per_week=days_per_week,
            workout_duration=workout_duration, equipment=equipment,
            dietary_pref=dietary_pref, allergies=profile.allergies,
            activity_level=activity_level, limitations=profile.limitations,
            workout_plan=existing_plan.workout_plan, 
            diet_plan=existing_plan.diet_plan, 
            ai_tips=existing_plan.ai_tips,
            bmi=profile.bmi,
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "plan": record,
            "profile_summary": _profile_summary(record),
            "cached": True
        })

    # ─── AI Generation (if no cache) ───
    try:
        workout_plan = ai.generate_workout_plan(profile)
        diet_plan = ai.generate_diet_plan(profile)
        tips = ai.generate_ai_tips(profile)
    except RuntimeError as exc:
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": str(exc)}, status_code=500
        )

    record = UserPlan(
        name=profile.name, age=age, gender=gender,
        weight=weight, height=height, goal=goal,
        fitness_level=fitness_level, workout_intensity=workout_intensity, days_per_week=days_per_week,
        workout_duration=workout_duration, equipment=equipment,
        dietary_pref=dietary_pref, allergies=profile.allergies,
        activity_level=activity_level, limitations=profile.limitations,
        workout_plan=workout_plan, diet_plan=diet_plan, ai_tips=tips,
        bmi=profile.bmi,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "plan": record,
        "profile_summary": _profile_summary(record),
    })


@app.post("/feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    plan_id: int = Form(...),
    feedback: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    plan = await db.get(UserPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    try:
        updated = ai.update_plan_with_feedback(
            original_workout=plan.workout_plan,
            original_diet=plan.diet_plan,
            feedback=feedback,
            profile_summary=_profile_summary(plan),
        )
    except RuntimeError as exc:
        return templates.TemplateResponse(
            "error.html", {"request": request, "error": str(exc)}, status_code=500
        )

    plan.feedback = feedback
    plan.updated_plan = updated
    plan.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(plan)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "plan": plan,
        "profile_summary": _profile_summary(plan),
        "feedback_applied": True,
    })


@app.get("/chat/{plan_id}", response_class=HTMLResponse)
async def chat_page(request: Request, plan_id: int, db: AsyncSession = Depends(get_db)):
    plan = await db.get(UserPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "plan": plan,
        "profile_summary": _profile_summary(plan),
    })


@app.post("/chat/{plan_id}/ask")
async def ask_coach(
    plan_id: int,
    question: str = Form(...),
    history: str = Form("[]"),
    db: AsyncSession = Depends(get_db),
):
    import json
    plan = await db.get(UserPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    try:
        parsed_history = json.loads(history)
    except Exception:
        parsed_history = []

    try:
        answer = ai.chat_with_coach(question, _profile_summary(plan), parsed_history)
    except RuntimeError as exc:
        return {"error": str(exc)}

    return {"answer": answer}


@app.get("/plans", response_class=HTMLResponse)
async def all_plans(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserPlan).order_by(desc(UserPlan.created_at)).limit(50))
    plans = result.scalars().all()
    return templates.TemplateResponse("plans.html", {"request": request, "plans": plans})


@app.get("/plan/{plan_id}", response_class=HTMLResponse)
async def view_plan(request: Request, plan_id: int, db: AsyncSession = Depends(get_db)):
    plan = await db.get(UserPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return templates.TemplateResponse("result.html", {
        "request": request,
        "plan": plan,
        "profile_summary": _profile_summary(plan),
    })


@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_TITLE, "version": APP_VERSION}
