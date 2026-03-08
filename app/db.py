from datetime import datetime
from sqlalchemy import Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class UserPlan(Base):
    """Stores every generated fitness plan with full profile snapshot."""
    __tablename__ = "user_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Profile
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(20))
    weight: Mapped[float] = mapped_column(Float)          # kg
    height: Mapped[float] = mapped_column(Float)          # cm
    goal: Mapped[str] = mapped_column(String(100))
    fitness_level: Mapped[str] = mapped_column(String(50))
    days_per_week: Mapped[int] = mapped_column(Integer)
    workout_duration: Mapped[int] = mapped_column(Integer)  # minutes
    equipment: Mapped[str] = mapped_column(String(500))
    dietary_pref: Mapped[str] = mapped_column(String(100))
    allergies: Mapped[str] = mapped_column(String(300), default="None")
    activity_level: Mapped[str] = mapped_column(String(50))
    limitations: Mapped[str] = mapped_column(String(300), default="None")

    # Generated content
    workout_plan: Mapped[str] = mapped_column(Text)
    diet_plan: Mapped[str] = mapped_column(Text)
    ai_tips: Mapped[str] = mapped_column(Text)

    # Feedback loop
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_plan: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Meta
    bmi: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
