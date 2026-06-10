"""
Structural validation.

Validates source code structure using Python's
Abstract Syntax Tree (AST).

Responsible for:
    - enforcing exercise constraints
    - detecting required syntax constructs
    - producing validation error codes

Not responsible for:
    - type checking
    - executing tests
"""

import ast


def assert_annotation(
    tree: ast.AST,
    variable_name: str,
    expected_type: str,
    error_code: str,
) -> None:
    """Asserts that a variable in the AST has the expected type annotation."""
    pass
