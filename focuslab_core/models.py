from pydantic import BaseModel, Field, field_validator
from typing import Literal

class Intake(BaseModel):
    problem: str = Field(default="", max_length=2500)
    task: str = Field(default="", max_length=300)
    available_minutes: int = Field(default=30, ge=5, le=240)
    distractions: list[str] = Field(default_factory=list, max_length=12)
    constraints: str = Field(default="", max_length=600)
    language: Literal["English", "Urdu", "Roman Urdu"] = "English"

class PlanStep(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    minutes: int = Field(ge=1, le=240)
    rationale: str = Field(max_length=500)

class FocusPlan(BaseModel):
    summary: str = Field(min_length=5, max_length=700)
    steps: list[PlanStep] = Field(min_length=1, max_length=8)
    environment_changes: list[str] = Field(default_factory=list, max_length=6)
    if_interrupted: str = Field(max_length=500)
    evidence_ids: list[str] = Field(default_factory=list, max_length=6)
    source: Literal["gemini", "local"] = "local"

    @field_validator("evidence_ids")
    @classmethod
    def clean_ids(cls, values):
        return list(dict.fromkeys(x for x in values if isinstance(x, str)))
