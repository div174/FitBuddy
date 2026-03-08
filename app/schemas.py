from pydantic import BaseModel, Field, field_validator
from typing import Optional


class FitnessProfileForm(BaseModel):
    """Validated input from the fitness profile form."""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=13, le=100)
    gender: str
    weight: float = Field(..., gt=20, lt=400)   # kg
    height: float = Field(..., gt=100, lt=280)  # cm
    goal: str
    fitness_level: str
    days_per_week: int = Field(..., ge=2, le=7)
    workout_duration: int = Field(..., ge=15, le=120)
    equipment: str   # comma-separated
    dietary_pref: str
    allergies: Optional[str] = "None"
    activity_level: str
    limitations: Optional[str] = "None"

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 1)

    @property
    def equipment_list(self) -> list[str]:
        return [e.strip() for e in self.equipment.split(",") if e.strip()]


class FeedbackForm(BaseModel):
    plan_id: int
    feedback: str = Field(..., min_length=5, max_length=1000)
