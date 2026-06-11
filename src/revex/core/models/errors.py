"""
Error models.

Defines schemas for validation failures and runtime errors.
"""

from pydantic import BaseModel, Field


class ValidationErrorRecord(BaseModel):
    """Represents a single validation check failure in an exercise."""

    error_code: str
    variable_name: str | None = Field(default=None)
    line_number: int | None = Field(default=None)
    message: str | None = Field(default=None)  # The localized hint/explanation


class ConfigError(Exception):
    """Exception raised for configuration syntax or validation errors."""

    pass


class ManifestError(Exception):
    """Exception raised for parsing errors found in manifest.json"""

    pass


class ExerciseNotFoundError(Exception):
    """Exception raised when an exercise is not found in the manifest or content directory."""

    pass
