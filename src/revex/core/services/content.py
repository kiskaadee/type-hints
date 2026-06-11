"""
Content loading layer.

Provides access to exercise resources stored
inside the bundled content directory.

Responsible for:
    - loading exercise source files
    - loading metadata
    - loading translations
    - loading solutions

Not responsible for:
    - discovering available exercises
    - tracking learner progress
    - validating submissions
"""

import json
from pathlib import Path

from revex.core.models.manifest import ManifestExercise
from revex.core.models.metadata import ExerciseMetadata
from revex.core.services.paths import PROJECT_ROOT


def get_exercise_name(exercise: ManifestExercise) -> str:
    """
    Helper to extract the exercise name from its path.
    Example: 'content/exercises/primitives.basic_type_hints' -> 'basic_type_hints'
    """
    folder_name = Path(exercise.path).name
    if "." in folder_name:
        return folder_name.split(".", 1)[1]
    return folder_name


def load_metadata(exercise: ManifestExercise) -> ExerciseMetadata:
    """Loads and parses the data.json metadata file inside the exercise directory."""
    data_path = PROJECT_ROOT / exercise.path / "data.json"
    if not data_path.is_file():
        raise FileNotFoundError(f"Metadata file not found: {data_path}")
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        return ExerciseMetadata(**data)
    except Exception as e:
        raise ValueError(
            f"Error parsing metadata for exercise '{exercise.id}': {e}"
        ) from e


def load_exercise_template(exercise: ManifestExercise) -> str:
    """Reads the raw exercise.pytxt template content."""
    template_path = PROJECT_ROOT / exercise.path / "exercise.pytxt"
    if not template_path.is_file():
        raise FileNotFoundError(f"Exercise template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def load_problem_description(exercise: ManifestExercise, lang: str = "en") -> str:
    """
    Reads problem.<lang>.md description content.
    Falls back to 'en' if the requested language description doesn't exist.
    """
    desc_path = PROJECT_ROOT / exercise.path / f"problem.{lang}.md"
    if not desc_path.is_file():
        desc_path = PROJECT_ROOT / exercise.path / "problem.en.md"
    if not desc_path.is_file():
        raise FileNotFoundError(
            f"Problem description not found for exercise '{exercise.id}'"
        )
    return desc_path.read_text(encoding="utf-8")


def load_solution(exercise: ManifestExercise) -> str:
    """Reads the raw solution.py content."""
    solution_path = PROJECT_ROOT / exercise.path / "solution.py"
    if not solution_path.is_file():
        raise FileNotFoundError(f"Solution file not found: {solution_path}")
    return solution_path.read_text(encoding="utf-8")
