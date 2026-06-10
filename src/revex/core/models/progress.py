"""
Progress models.

Defines the structure of learner progress data.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ExerciseProgress(BaseModel):
    """Detailed completion metrics for a single exercise."""

    completed: bool = Field(default=False)
    completed_at: datetime | None = Field(default=None)
    attempts: int = Field(default=0)


class Progress(BaseModel):
    """Overall progress tracking schema for progress.json."""

    completed_exercises: dict[str, ExerciseProgress] = Field(default_factory=dict)
