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
