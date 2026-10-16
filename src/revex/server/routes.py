"""
FastAPI route handlers for revex-server.
"""

from fastapi import APIRouter, HTTPException, Query

from revex.core.models import ExerciseNotFoundError
from revex.server.schemas import (
    CheckRequest,
    CheckResponse,
    ExerciseCatalogResponse,
    ExerciseDetailResponse,
)
from revex.server.services import (
    check_solution,
    get_catalog,
    get_exercise_detail,
)

router = APIRouter(prefix="/api/v1")


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check ping endpoint."""
    return {"status": "ok", "service": "revex-server"}


@router.get("/exercises", response_model=ExerciseCatalogResponse)
def list_exercises(
    lang: str = Query(default="en", pattern="^(en|es)$")
) -> ExerciseCatalogResponse:
    """Returns the course catalog with sequence order and completion states."""
    try:
        return get_catalog(lang=lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load catalog: {e}")


@router.get("/exercises/{exercise_id}", response_model=ExerciseDetailResponse)
def get_exercise(
    exercise_id: str,
    lang: str = Query(default="en", pattern="^(en|es)$"),
) -> ExerciseDetailResponse:
    """Returns exercise metadata, problem guide markdown, and starter code."""
    try:
        return get_exercise_detail(exercise_id, lang=lang)
    except ExerciseNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Exercise '{exercise_id}' not found in course catalog.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load exercise details: {e}"
        )


@router.post("/check", response_model=CheckResponse)
def validate_code(
    payload: CheckRequest,
    lang: str = Query(default="en", pattern="^(en|es)$"),
) -> CheckResponse:
    """
    Statelessly validates user code against AST rules and strict Pyright.
    Returns column coordinates for Monaco squiggly underlines and ANSI terminal text.
    """
    try:
        return check_solution(
            exercise_id=payload.exercise_id,
            code=payload.code,
            lang=lang,
        )
    except ExerciseNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Exercise '{payload.exercise_id}' not found in course catalog.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Validation execution failed: {e}"
        )
