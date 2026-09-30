"""Pydantic models for validation."""
from pydantic import BaseModel, Field, field_validator


class UserInput(BaseModel):
    username: str = Field(..., min_length=1)
    user_id: int
    age: int = Field(..., gt=0, lt=120)
    weight: float = Field(..., gt=0)
    goal: str = Field(..., min_length=1)
    intensity: str

    @field_validator("intensity")
    @classmethod
    def check_intensity(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in {"low", "medium", "high"}:
            raise ValueError("intensity must be low, medium or high")
        return v


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., min_length=1)


class WorkoutRequest(BaseModel):
    goal: str
    intensity: str
