"""
Domain service functions for the revex web server.
"""

import tempfile
import time
from pathlib import Path

from revex.core.models import ValidationErrorRecord
from revex.core.services.content import (
    get_exercise_name,
    load_metadata,
    load_problem_description,
)
from revex.core.services.manifest import (
    get_manifest_exercise,
    load_manifest,
)
from revex.core.services.paths import PROJECT_ROOT
from revex.core.services.progress import (
    get_progress_statistics,
    load_progress,
    record_attempt,
)
from revex.core.validators.ast_validator import validate_ast
from revex.core.validators.pyright_validator import validate_pyright
from revex.server.schemas import (
    CheckErrorItem,
    CheckResponse,
    ExerciseCatalogResponse,
    ExerciseDetailResponse,
    ExerciseListItem,
)


def get_catalog(lang: str = "en") -> ExerciseCatalogResponse:
    """Returns the ordered exercise catalog with completion states."""
    manifest = load_manifest()
    progress = load_progress()

    items: list[ExerciseListItem] = []
    for idx, ex in enumerate(manifest.exercises, start=1):
        try:
            meta = load_metadata(ex)
            trans = meta.translations.get(lang) or meta.translations.get("en")
            title = trans.title if trans else get_exercise_name(ex).replace("_", " ").title()
        except Exception:
            title = get_exercise_name(ex).replace("_", " ").title()

        ep = progress.completed_exercises.get(ex.id)
        status = "not_started"
        if ep and ep.completed:
            status = "completed"
        elif ep and ep.attempts > 0:
            status = "in_progress"

        group_title = ex.group.replace("_", " ").title()
        slug = f"{ex.id}-{get_exercise_name(ex).replace('_', '-')}"

        items.append(
            ExerciseListItem(
                id=ex.id,
                slug=slug,
                group=ex.group,
                group_title=group_title,
                order=idx,
                title=title,
                difficulty=ex.difficulty,
                status=status,
            )
        )

    stats = get_progress_statistics()
    overall = stats.get("overall", {"completed": 0, "total": len(items), "attempts": 0})
    completed_count = sum(
        1 for p in progress.completed_exercises.values() if p.completed
    )

    return ExerciseCatalogResponse(
        exercises=items,
        current_streak=completed_count,
        total_solved=overall.get("completed", completed_count),
        total_exercises=overall.get("total", len(items)),
    )


def get_exercise_detail(exercise_id: str, lang: str = "en") -> ExerciseDetailResponse:
    """Returns full exercise details, markdown problem description, and starter code."""
    manifest = load_manifest()
    exercise = get_manifest_exercise(exercise_id)
    metadata = load_metadata(exercise)
    progress = load_progress()

    # Determine prev and next exercise IDs
    ex_ids = [e.id for e in manifest.exercises]
    idx = ex_ids.index(exercise_id) if exercise_id in ex_ids else -1
    prev_id = ex_ids[idx - 1] if idx > 0 else None
    next_id = ex_ids[idx + 1] if 0 <= idx < len(ex_ids) - 1 else None

    # Load problem markdown
    problem_md = load_problem_description(exercise, lang=lang)

    # Load starter code template
    exercise_path = PROJECT_ROOT / exercise.path
    template_path = exercise_path / "exercise.pytxt"
    starter_code = (
        template_path.read_text(encoding="utf-8")
        if template_path.is_file()
        else "# Exercise starter code not found.\n"
    )

    # Extract hints from translation
    trans = metadata.translations.get(lang) or metadata.translations.get("en")
    title = trans.title if trans else get_exercise_name(exercise).replace("_", " ").title()
    hints: list[str] = []
    if trans and trans.hints:
        for hint_text in trans.hints.get("error_codes", {}).values():
            hints.append(hint_text)

    ep = progress.completed_exercises.get(exercise.id)
    is_completed = ep.completed if ep else False

    return ExerciseDetailResponse(
        id=exercise.id,
        title=title,
        group=exercise.group,
        problem_markdown=problem_md,
        starter_code=starter_code,
        saved_code=None,
        hints=hints,
        prev_exercise_id=prev_id,
        next_exercise_id=next_id,
        completed=is_completed,
    )


def check_solution(exercise_id: str, code: str, lang: str = "en") -> CheckResponse:
    """
    Statelessly validates user code against AST rules and Pyright strict type safety.
    Returns structured column-precise markers and colorized ANSI terminal output.
    """
    start_time = time.perf_counter()
    manifest = load_manifest()
    exercise = get_manifest_exercise(exercise_id)
    metadata = load_metadata(exercise)

    # Determine next exercise id
    ex_ids = [e.id for e in manifest.exercises]
    idx = ex_ids.index(exercise_id) if exercise_id in ex_ids else -1
    next_id = ex_ids[idx + 1] if 0 <= idx < len(ex_ids) - 1 else None

    # Write code to an ephemeral temp file
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = Path(tmp.name)

    raw_errors: list[ValidationErrorRecord] = []
    try:
        # Phase 1: AST validation
        ast_errors = validate_ast(tmp_path, metadata.validation)
        raw_errors.extend(ast_errors)

        # Phase 2: Pyright validation (only if AST passes cleanly)
        if not ast_errors:
            pyright_errors = validate_pyright(tmp_path)
            raw_errors.extend(pyright_errors)

    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    # Map localized error hints
    trans = metadata.translations.get(lang) or metadata.translations.get("en")
    hints_dict = trans.hints.get("error_codes", {}) if trans and trans.hints else {}
    for err in raw_errors:
        if err.error_code in hints_dict:
            err.message = hints_dict[err.error_code]

    passed = len(raw_errors) == 0
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Record progress attempt
    record_attempt(exercise_id, completed=passed)
    progress = load_progress()

    # Format ANSI terminal output
    output_lines: list[str] = [
        "\u001b[36m~\u001b[0m",
        f"\u001b[33m-> revex check {exercise_id}\u001b[0m",
    ]

    error_items: list[CheckErrorItem] = []
    if passed:
        output_lines.append(
            f"\u001b[32m[PASS]\u001b[0m All type rules and AST invariants satisfied! ({elapsed_ms}ms)"
        )
        if next_id:
            output_lines.append(f"\u001b[90mNext exercise unlocked: {next_id}\u001b[0m")
    else:
        output_lines.append(
            f"\u001b[31m[FAIL]\u001b[0m Validation failed with {len(raw_errors)} error(s):"
        )
        for err in raw_errors:
            msg = err.message or "Validation check failed."
            msg = msg.replace(str(tmp_path), "solution.py").replace(str(PROJECT_ROOT), "<revex>")
            pos_str = f"Line {err.line_number}" if err.line_number else ""
            if err.column_number:
                pos_str += f":{err.column_number}"
            output_lines.append(f"  \u001b[31m✗\u001b[0m {pos_str} - {msg} \u001b[90m[{err.error_code}]\u001b[0m")

            error_items.append(
                CheckErrorItem(
                    start_line=err.line_number,
                    start_column=err.column_number,
                    end_line=err.end_line_number or err.line_number,
                    end_column=err.end_column_number or (err.column_number + 1 if err.column_number else None),
                    message=msg,
                    error_code=err.error_code,
                    severity="error",
                )
            )

    completed_count = sum(
        1 for p in progress.completed_exercises.values() if p.completed
    )
    stats = {
        "total_completed": completed_count,
        "streak": completed_count,
    }

    return CheckResponse(
        passed=passed,
        execution_time_ms=elapsed_ms,
        terminal_output="\n".join(output_lines),
        errors=error_items,
        next_exercise_id=next_id if passed else None,
        stats=stats,
    )
