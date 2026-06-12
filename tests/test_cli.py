from unittest.mock import patch

from revex.main import main

def run_cli_main(args: list[str]) -> None:
    with patch("sys.argv", ["revex"] + args):
        try:
            main()
        except SystemExit as e:
            if e.code != 0:
                raise RuntimeError(f"CLI exited with non-zero code: {e.code}")

def test_init_command(capsys):
    run_cli_main(["init"])
    captured = capsys.readouterr()
    assert "Initializing local workspace..." in captured.out
    assert "Environment successfully initialized!" in captured.out

def test_sync_command(capsys):
    run_cli_main(["init"])
    capsys.readouterr()  # clear buffer
    
    run_cli_main(["sync"])
    captured = capsys.readouterr()
    assert "Synchronizing workspace exercises..." in captured.out
    assert "Added:   1" in captured.out

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
    assert "cd workspace/primitives/0101-basic_type_hints" in captured.out

def test_check_and_status_flow(capsys):
    run_cli_main(["init"])
    run_cli_main(["sync"])
    capsys.readouterr()
    
    from revex.core.services.paths import WORKSPACE_DIR, PROJECT_ROOT
    exercise_file = WORKSPACE_DIR / "primitives/0101-basic_type_hints/basic_type_hints.py"
    
    # Ensure checking fails initially due to syntax error in template
    run_cli_main(["check", str(exercise_file)])
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
    assert "1/1 (100.0%)" in captured.out
