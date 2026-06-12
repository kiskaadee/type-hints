"""
Type checking validation engine.

Validates source code type annotations by executing Pyright as a
subprocess and parsing its diagnostic output.

Responsible for:
    - Executing the Pyright CLI against target source files.
    - Safely parsing and typing dynamic JSON diagnostic output.
    - Translating Pyright errors into standard validation records.

Not responsible for:
    - Structural or logic validation (handled by AST).
    - Runtime execution or unit testing.
    - Installing or managing the Pyright dependency itself.
"""

import json
import subprocess
from pathlib import Path
from typing import TypedDict, cast

from revex.core.models import ValidationErrorRecord


# 1. Define the expected shape of the Pyright JSON output
class PyrightPosition(TypedDict, total=False):
    line: int
    character: int


class PyrightRange(TypedDict, total=False):
    start: PyrightPosition
    end: PyrightPosition


class PyrightDiagnostic(TypedDict, total=False):
    severity: str
    message: str
    rule: str
    range: PyrightRange


class PyrightOutput(TypedDict, total=False):
    generalDiagnostics: list[PyrightDiagnostic]


def validate_pyright(file_path: Path) -> list[ValidationErrorRecord]:
    """
    Execute Pyright type checking and parse the results.

    Runs `pyright --outputjson` as a subprocess against the target file.
    Captures the JSON stdout and maps any diagnostic events marked with
    severity 'error' into standard ValidationErrorRecord objects.

    Args:
        file_path: The filesystem path to the Python file to check.

    Returns:
        A list of ValidationErrorRecord objects representing type errors.
        Returns an empty list if the file passes all type checks.
    """
    errors: list[ValidationErrorRecord] = []

    try:
        # Run pyright with json output
        result = subprocess.run(
            ["pyright", "--outputjson", str(file_path)],
            capture_output=True,
            text=True,
        )

        stdout = result.stdout.strip()
        if not stdout:
            if result.stderr:
                errors.append(
                    ValidationErrorRecord(
                        error_code="PYRIGHT_EXECUTION_ERROR",
                        message=f"Pyright failed to run: {result.stderr.strip()}",
                    )
                )
            return errors

        # 2 - Parse the JSON and cast it to the strictly typed dictionary
        data = cast(PyrightOutput, json.loads(stdout))
        # data = json.loads(stdout)
        diagnostics = data.get("generalDiagnostics", [])

        for diag in diagnostics:
            severity = diag.get("severity")
            if severity == "error":
                message = diag.get("message", "Type check failed.")
                rule = diag.get("rule", "typecheck")

                range_info = diag.get("range", {})
                start_info = range_info.get("start", {})
                line_no = start_info.get("line", 0) + 1  # Convert to 1-indexed

                errors.append(
                    ValidationErrorRecord(
                        error_code=f"PYRIGHT_{rule.upper()}",
                        line_number=line_no,
                        message=message,
                    )
                )
    except json.JSONDecodeError as e:
        errors.append(
            ValidationErrorRecord(
                error_code="PYRIGHT_PARSE_ERROR",
                message=f"Failed to parse Pyright JSON output: {e}",
            )
        )
    except Exception as e:
        errors.append(
            ValidationErrorRecord(
                error_code="PYRIGHT_EXECUTION_ERROR",
                message=f"Failed to run Pyright type checker: {e}",
            )
        )

    return errors
