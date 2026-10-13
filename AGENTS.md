# Project Guidelines & Safety Rules for AI Agents

## 1. Mission & Authority

**type-hints (`revex`)** is a local-first interactive CLI platform and laboratory for practicing modern Python type hints through progressive exercises, AST structural checks, and strict Pyright validation.
- **Architecture Documentation** (`src/revex/docs/architecture.md`), **Authoring Guide** (`src/revex/docs/authoring_guide.md`), and **Course Outline** (`docs/outline.md`) define the authoritative design.
- **Curriculum & Core Engine Integrity:** Do not remove existing exercises, alter canonical paths, or weaken Pyright strictness without explicit authorization.

---

## 2. Working Tree Authority & Safety (MANDATORY)

The working tree represents the user's active work.
1. **Inspect First:** Run `git status` and inspect target files before modifying or creating anything.
2. **Branch Discipline:** Never commit directly to `main`. Create or use feature branches (e.g., `feat/*`, `fix/*`).
3. **No Destructive Git Commands:** Never run `reset --hard`, `clean -fd`, `restore`, `checkout`, `stash`, `rebase`, or `push --force` without explicit yes.
4. **Preserve User Workspace:** Files in `workspace/` and `.user_data/` belong to the learner. Never overwrite learner code during sync or validation tasks.
5. **Live Task Tracking (`todo.txt`):** Keep `todo.txt` synchronized with code reality. When a task or milestone deliverable is implemented and verified, mark it as completed (`x YYYY-MM-DD ...`) immediately. The file must remain in standard Todo.txt format without comments or markdown headers so it can be parsed by shell wrappers (`todo.sh`) and `tuxedo`.
6. **Pre-Commit Safeguard:** Never stage or commit code that has not passed the full Safeguard Gate (Ruff + Pyright + Pytest).
7. **Final Diff Verification:** Before completing work, verify `git status` and `git diff` to ensure no unintended modifications occurred.

---

## 3. Operational & Domain Invariants

### 3.1 Content & Storage Boundaries
- **Canonical Content:** Stored under `content/exercises/<group>.<exercise_name>/`.
- **Manifest:** Authoritative registry is [content/manifest.json](content/manifest.json). Every exercise must have a unique 4-digit ID (e.g., `0501`).
- **Exercise Structure:** Every exercise directory must contain:
  - `data.json`: Validation rules, AST specs, and bilingual error hints.
  - `exercise.pytxt`: Exercise template copied to learner workspaces.
  - `solution.py`: Reference solution passing strict Pyright and AST validation.
  - `problem.en.md`: English problem description and syntax explanation.
  - `problem.es.md`: Spanish problem description.
- **Learner Workspace:** Located in `workspace/` (git-ignored). Synchronized via `revex sync`.

### 3.2 Code Quality & Tooling
- **Package Management:** Use `uv` exclusively. Do not use raw `pip` or modify `uv.lock` manually.
- **Formatting & Linting:** Code must pass `uv run ruff check .` with zero errors.
- **Type Checking:** All source code (`src/`) and reference solutions (`content/exercises/**/solution.py`) must pass `uv run pyright .` in strict mode.
- **Test Suite:** Automated tests must pass: `uv run pytest`.

---

## 4. Development Safeguard Workflow (MANDATORY GATE)

Before declaring any task complete or staging any commit, all code and content must pass the automated development safeguard gate:

1. **Linting & Code Formatting:**
   ```bash
   uv run ruff check .
   ```
   Zero errors or warnings permitted.

2. **Strict Type Safety Analysis:**
   ```bash
   uv run pyright .
   ```
   Both the engine codebase (`src/`) and all canonical reference solutions (`content/exercises/**/solution.py`) must pass in strict mode with zero errors, warnings, or untyped leaks.

3. **Automated Test Suite:**
   ```bash
   uv run pytest
   ```
   All unit, CLI, and integration tests must pass cleanly.

4. **Exercise Verification:**
   - If an exercise was created or modified: verify that its `solution.py` passes AST validation and Pyright, and verify that `exercise.pytxt` produces the expected pedagogical errors.

5. **Task Synchronization (`todo.txt`):**
   - Update `todo.txt` immediately upon verifying a deliverable (`x YYYY-MM-DD ...`).
