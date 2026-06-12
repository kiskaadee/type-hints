"""
Error models.

Defines schemas for validation failures and runtime errors.
"""

from pydantic import BaseModel, Field


class ValidationErrorRecord(BaseModel):
    """
    Data Transfer Object (DTO) representing a single validation check failure.

    Used to safely serialize the results of an AST structural check so they
    can be sent over the network, saved to files, or printed to stdout.
    """

    error_code: str
    variable_name: str | None = Field(default=None)
    line_number: int | None = Field(default=None)
    message: str | None = Field(default=None)  # The localized hint/explanation


class ASTValidationError(Exception):
    """
    Control-flow exception raised during AST validation rules checking.

    Unlike ValidationErrorRecord (which reports user mistakes), this exception
    is caught internally by the validator to halt the current check and map
    the failure into a safe DTO.
    """

    error_code: str
    variable_name: str
    line_number: int | None

    def __init__(
        self,
        error_code: str,
        variable_name: str,
        line_number: int | None,
        message: str,
    ) -> None:
        self.error_code = error_code
        self.variable_name = variable_name
        self.line_number = line_number
        super().__init__(message)


class ConfigError(Exception):
    """Exception raised for configuration syntax or validation errors."""

    pass


class ManifestError(Exception):
    """Exception raised for parsing errors found in manifest.json"""

    pass


class ExerciseNotFoundError(Exception):
    """Exception raised when an exercise is not found in the manifest or content directory."""

    pass


class ProgressError(Exception):
    """Exception raised for progress data syntax or validation errors."""

    pass

