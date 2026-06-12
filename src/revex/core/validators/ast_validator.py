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
from pathlib import Path

from revex.core.models import ASTValidationError, ValidationErrorRecord, ValidationSpec


def assert_annotation(
    tree: ast.AST,
    variable_name: str,
    expected_type: str,
    error_code: str,
) -> None:
    """
    Check an AST for a specifically annotated variable assignment.

    Traverses the provided AST to find assignments matching `variable_name`.
    Verifies that the variable is both present and explicitly annotated
    with the `expected_type`.

    Args:
        tree: The parsed Python Abstract Syntax Tree to inspect.
        variable_name: The target identifier to search for (e.g., 'count').
        expected_type: The required type hint as a string (e.g., 'int').
        error_code: The domain-specific error code to include on failure.

    Raises:
        ASTValidationError: If the variable is missing entirely, exists but
            lacks an annotation, or has a mismatched type hint.
    """
    ann_assign_nodes: list[ast.AnnAssign] = []  # store annotated assignments
    assign_nodes: list[ast.Assign] = []  # store standard assignments

    # ast.walk visits every node in the Abstract Syntax Tree
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == variable_name:
                ann_assign_nodes.append(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    assign_nodes.append(node)

    if not ann_assign_nodes:
        if assign_nodes:
            # Variable exists but is not annotated
            line_no = assign_nodes[0].lineno
            raise ASTValidationError(
                error_code=error_code,
                variable_name=variable_name,
                line_number=line_no,
                message=f"Variable '{variable_name}' is missing a type annotation.",
            )
        else:
            raise ASTValidationError(
                error_code=error_code,
                variable_name=variable_name,
                line_number=None,
                message=f"Variable '{variable_name}' is missing or not defined.",
            )

    # Check the first annotation assignment found
    node = ann_assign_nodes[0]
    actual_type = ast.unparse(node.annotation).strip()
    if actual_type != expected_type.strip():
        raise ASTValidationError(
            error_code=error_code,
            variable_name=variable_name,
            line_number=node.lineno,
            message=f"Expected type hint '{expected_type}' but found '{actual_type}'.",
        )


def validate_ast(file_path: Path, spec: ValidationSpec) -> list[ValidationErrorRecord]:
    """
    Parse a source file and execute structural validation rules.

    Serves as the main entry point for static AST checks. Safely handles
    missing files and syntax errors, converting all control-flow exceptions
    into standardized data transfer objects (DTOs).

    Args:
        file_path: The filesystem path to the student's source code.
        spec: The rulebook containing the expected variables and their types.

    Returns:
        A list of ValidationErrorRecord objects detailing any failures.
        Returns an empty list if all structural checks pass perfectly.
    """
    errors: list[ValidationErrorRecord] = []

    if not file_path.is_file():
        errors.append(
            ValidationErrorRecord(
                error_code="FILE_NOT_FOUND",
                message=f"Solution file not found: {file_path}",
            )
        )
        return errors

    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
    except SyntaxError as e:
        errors.append(
            ValidationErrorRecord(
                error_code="SYNTAX_ERROR",
                line_number=e.lineno,
                message=f"Syntax Error: {e.msg}",
            )
        )
        return errors
    except Exception as e:
        errors.append(
            ValidationErrorRecord(
                error_code="PARSING_ERROR",
                message=f"Failed to parse source file: {e}",
            )
        )
        return errors

    for variable_name, rule in spec.annotations.items():
        try:
            assert_annotation(tree, variable_name, rule.type, rule.error_code)
        except ASTValidationError as e:
            errors.append(
                ValidationErrorRecord(
                    error_code=e.error_code,
                    variable_name=e.variable_name,
                    line_number=e.line_number,
                    message=str(e),
                )
            )

    return errors
