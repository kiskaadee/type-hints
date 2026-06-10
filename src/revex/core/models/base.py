import re
from typing import Literal

from pydantic import BaseModel, field_validator


class ExerciseBase(BaseModel):
    id: str
    group: str
    difficulty: Literal["beginner", "intermediate", "advanced"]

    # enforce 4-digit format for exercise Id.
    @field_validator("id")
    @classmethod
    def validate_id_format(cls, value: str) -> str:
        if not re.match(r"^\d{4}$", value):
            raise ValueError("ID must be exactly 4 digits (e.g., '0101')")
        return value
