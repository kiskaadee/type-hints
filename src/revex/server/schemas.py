"""
Pydantic API schemas for revex-server.
"""

from typing import Literal
from pydantic import BaseModel, Field


class ExerciseListItem(BaseModel):
    id: str
    slug: str
    group: str
    group_title: str
    order: int
    title: str
    difficulty: str
    status: Literal["not_started", "in_progress", "completed"] = "not_started"


class ExerciseCatalogResponse(BaseModel):
    exercises: list[ExerciseListItem]
    current_streak: int = 0
    total_solved: int = 0
    total_exercises: int = 0


class ExerciseDetailResponse(BaseModel):
    id: str
    title: str
    group: str
    problem_markdown: str
    starter_code: str
    saved_code: str | None = None
    hints: list[str] = Field(default_factory=list[str])
    prev_exercise_id: str | None = None
    next_exercise_id: str | None = None
    completed: bool = False


class CheckRequest(BaseModel):
    exercise_id: str
    code: str


class CheckErrorItem(BaseModel):
    start_line: int | None = None
    start_column: int | None = None
    end_line: int | None = None
    end_column: int | None = None
    message: str
    error_code: str
    severity: Literal["error", "warning"] = "error"


class CheckResponse(BaseModel):
    passed: bool
    execution_time_ms: float
    terminal_output: str
    errors: list[CheckErrorItem] = Field(default_factory=list[CheckErrorItem])
    next_exercise_id: str | None = None
    stats: dict[str, int] | None = None
