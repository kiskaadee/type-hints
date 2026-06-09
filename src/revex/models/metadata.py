"""
Exercise models.

Defines the structure of exercise metadata
and content descriptors.
"""

from pydantic import BaseModel, Field

from .base import ExerciseBase


class AnnotationRule(BaseModel):
    """AST validation rule for verifying the type hint of a variable."""

    type: str
    error_code: str


class ValidationSpec(BaseModel):
    """Declarative validation specifications for an exercise."""

    annotations: dict[str, AnnotationRule] = Field(default_factory=dict)


class ExerciseTranslation(BaseModel):
    """Language translation information for exercise descriptions and hints."""

    title: str
    hints: dict[str, dict[str, str]] = Field(default_factory=dict)


class ExerciseMetadata(ExerciseBase):
    """Schema representing complete metadata stored inside data.json."""

    tags: list[str] = Field(default_factory=list)
    validation: ValidationSpec = Field(default_factory=ValidationSpec)
    translations: dict[str, ExerciseTranslation] = Field(default_factory=dict)
