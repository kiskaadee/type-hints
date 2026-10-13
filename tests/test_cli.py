from unittest.mock import patch

from revex.main import main

def run_cli_main(args: list[str]) -> None:
    with patch("sys.argv", ["revex"] + args):
        try:
            main()
        except SystemExit as e:
            if e.code != 0:
                raise RuntimeError(f"CLI exited with non-zero code: {e.code}")

def test_empty_command_shows_help(capsys):
    import pytest
    with patch("sys.argv", ["revex"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "usage: " in captured.out or "usage: " in captured.err

def test_help_command(capsys):
    run_cli_main(["help", "check"])
    captured = capsys.readouterr()
    assert "usage: revex check" in captured.out

def test_init_command(capsys):
    run_cli_main(["init"])
    captured = capsys.readouterr()
    assert "Initializing local workspace..." in captured.out
    assert "Environment successfully initialized!" in captured.out

def test_sync_command(capsys):
    from revex.core.services.manifest import load_manifest

    run_cli_main(["init"])
    capsys.readouterr()  # clear buffer

    run_cli_main(["sync"])
    captured = capsys.readouterr()
    manifest = load_manifest()
    assert "Synchronizing workspace exercises..." in captured.out
    assert f"Added:   {len(manifest.exercises)}" in captured.out

def test_set_command(capsys):
    run_cli_main(["init"])
    capsys.readouterr()
    
    # Check default config
    run_cli_main(["set"])
    captured = capsys.readouterr()
    assert "Language: en" in captured.out
    assert "Allow Hints: True" in captured.out
    
    # Update language
    run_cli_main(["set", "--language", "es"])
    captured = capsys.readouterr()
    assert "Setting 'language' successfully set to: es" in captured.out
    
    # Verify update
    run_cli_main(["set"])
    captured = capsys.readouterr()
    assert "Language: es" in captured.out
    
    # Try invalid allow-llm update
    run_cli_main(["set", "--allow-llm", "true"])
    captured = capsys.readouterr()
    assert "LLM-powered interactive hints are not yet supported" in captured.out

def test_view_command(capsys):
    run_cli_main(["init"])
    run_cli_main(["sync"])
    capsys.readouterr()
    
    run_cli_main(["view", "0101"])
    captured = capsys.readouterr()
    assert "0101" in captured.out
    assert "Exercise workspace:" in captured.out
    assert "workspace/primitives/0101-basic_type_hints" in captured.out

def test_check_and_status_flow(capsys):
    run_cli_main(["init"])
    run_cli_main(["sync"])
    capsys.readouterr()
    
    from revex.core.services.paths import WORKSPACE_DIR, PROJECT_ROOT
    exercise_file = WORKSPACE_DIR / "primitives/0101-basic_type_hints/basic_type_hints.py"
    
    # Ensure checking fails initially in template
    run_cli_main(["check", str(exercise_file)])
    captured = capsys.readouterr()
    assert "Validation failed" in captured.out

    # Ensure we can check using the exercise ID directly
    run_cli_main(["check", "0101"])
    captured = capsys.readouterr()
    assert "Validation failed" in captured.out
    
    # Copy correct solution to simulate user solving the exercise
    solution_file = PROJECT_ROOT / "content/exercises/primitives.basic_type_hints/solution.py"
    exercise_file.write_text(solution_file.read_text(encoding="utf-8"), encoding="utf-8")
    
    # Check again (should pass)
    run_cli_main(["check", str(exercise_file)])
    captured = capsys.readouterr()
    assert "All checks passed! Lesson completed." in captured.out
    
    # Verify status
    run_cli_main(["status"])
    captured = capsys.readouterr()
    assert "Revex Progress Status" in captured.out
    assert "primitives" in captured.out
    assert "1/6 (16.7%)" in captured.out


def test_function_signature_validator():
    import tempfile
    from pathlib import Path
    from revex.core.models.metadata import ValidationSpec, FunctionRule
    from revex.core.validators.ast_validator import validate_ast
    
    spec = ValidationSpec(
        functions={
            "close_ticket": FunctionRule(
                params={"agent": "str"},
                returns="None",
                error_code="TEST_ERR_SIG"
            )
        }
    )
    
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        try:
            # 1. Invalid signature (missing return annotation)
            tmp_path.write_text("def close_ticket(agent: str):\n    pass\n", encoding="utf-8")
            errors = validate_ast(tmp_path, spec)
            assert len(errors) == 1
            assert errors[0].error_code == "TEST_ERR_SIG"
            assert "missing a return type annotation" in errors[0].message
            
            # 2. Invalid signature (mismatched parameter annotation)
            tmp_path.write_text("def close_ticket(agent: str | None) -> None:\n    pass\n", encoding="utf-8")
            errors = validate_ast(tmp_path, spec)
            assert len(errors) == 1
            assert "Expected parameter 'agent'" in errors[0].message
            
            # 3. Invalid signature (missing parameter)
            tmp_path.write_text("def close_ticket() -> None:\n    pass\n", encoding="utf-8")
            errors = validate_ast(tmp_path, spec)
            assert len(errors) == 1
            assert "missing the expected parameter" in errors[0].message

            # 4. Valid signature
            tmp_path.write_text("def close_ticket(agent: str) -> None:\n    pass\n", encoding="utf-8")
            errors = validate_ast(tmp_path, spec)
            assert len(errors) == 0
        finally:
            tmp_path.unlink()


def test_sync_restore_command(capsys):
    run_cli_main(["init"])
    run_cli_main(["sync"])
    capsys.readouterr()

    from revex.core.services.paths import WORKSPACE_DIR
    exercise_file = WORKSPACE_DIR / "primitives/0101-basic_type_hints/basic_type_hints.py"

    # Write a modification
    exercise_file.write_text("MODIFIED_BY_USER", encoding="utf-8")

    # Run restore sync
    run_cli_main(["sync", "--restore", "0101"])
    captured = capsys.readouterr()
    assert "Restoring exercise workspace [0101]..." in captured.out
    assert "Restored: 1" in captured.out
    
    # Check that it's back to original template
    restored_content = exercise_file.read_text(encoding="utf-8")
    assert restored_content != "MODIFIED_BY_USER"
    assert "Exercise 0101" in restored_content

    # Run restore with invalid ID
    run_cli_main(["sync", "--restore", "9999"])
    captured = capsys.readouterr()
    assert "Error executing workspace synchronization:" in captured.out
    assert "not found in the content registry" in captured.out
