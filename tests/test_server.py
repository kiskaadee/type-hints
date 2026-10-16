"""
Integration tests for the revex FastAPI web server.
"""

from fastapi.testclient import TestClient

from revex.server.app import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "revex-server"}


def test_list_exercises() -> None:
    response = client.get("/api/v1/exercises")
    assert response.status_code == 200
    data = response.json()
    assert "exercises" in data
    assert len(data["exercises"]) >= 13
    first_ex = data["exercises"][0]
    assert first_ex["id"] == "0101"
    assert "slug" in first_ex
    assert "group" in first_ex
    assert "order" in first_ex


def test_get_exercise_detail_success() -> None:
    response = client.get("/api/v1/exercises/0501")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "0501"
    assert "Modern Generics" in data["title"]
    assert "# Exercise 0501" in data["problem_markdown"]
    assert "first_or_default" in data["starter_code"]
    assert data["prev_exercise_id"] == "0206"


def test_get_exercise_detail_not_found() -> None:
    response = client.get("/api/v1/exercises/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_check_solution_failure() -> None:
    # Submit starter code with deliberate errors
    payload = {
        "exercise_id": "0501",
        "code": "def first_or_default(items, default):\n    return items[0]\n",
    }
    response = client.post("/api/v1/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is False
    assert len(data["errors"]) > 0
    err = data["errors"][0]
    assert "start_line" in err
    assert "start_column" in err
    assert "terminal_output" in data
    assert "[FAIL]" in data["terminal_output"]


def test_check_solution_success() -> None:
    # Submit canonical solution passing all AST and Pyright checks
    from revex.core.services.paths import PROJECT_ROOT

    solution_file = PROJECT_ROOT / "content/exercises/generics.pep695_generics/solution.py"
    solution_code = solution_file.read_text(encoding="utf-8")

    payload = {
        "exercise_id": "0501",
        "code": solution_code,
    }
    response = client.post("/api/v1/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is True
    assert data["errors"] == []
    assert "[PASS]" in data["terminal_output"]
    assert data["stats"] is not None
