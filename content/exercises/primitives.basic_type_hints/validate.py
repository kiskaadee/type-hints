"""
Exercise 0101 Validation

Checks that all variables use the expected primitive type
annotations.

This file is intentionally exercise-specific.
The generic validation runner loads and executes it.
"""

from revex.validators.ast_validator import assert_annotation


def validate(tree) -> None:
    assert_annotation(
        tree,
        variable_name="employee_name",
        expected_type="str",
        error_code="PRIMITIVE_STR_001",
    )

    assert_annotation(
        tree,
        variable_name="job_title",
        expected_type="str",
        error_code="PRIMITIVE_STR_002",
    )

    assert_annotation(
        tree,
        variable_name="employee_id",
        expected_type="int",
        error_code="PRIMITIVE_INT_001",
    )

    assert_annotation(
        tree,
        variable_name="age",
        expected_type="int",
        error_code="PRIMITIVE_INT_002",
    )

    assert_annotation(
        tree,
        variable_name="hourly_rate",
        expected_type="float",
        error_code="PRIMITIVE_FLOAT_001",
    )

    assert_annotation(
        tree,
        variable_name="hours_per_week",
        expected_type="float",
        error_code="PRIMITIVE_FLOAT_002",
    )

    assert_annotation(
        tree,
        variable_name="is_full_time",
        expected_type="bool",
        error_code="PRIMITIVE_BOOL_001",
    )

    assert_annotation(
        tree,
        variable_name="completed_orientation",
        expected_type="bool",
        error_code="PRIMITIVE_BOOL_002",
    )
