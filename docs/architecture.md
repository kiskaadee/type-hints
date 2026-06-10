# Architecture Decision Log

This document records the major design and architectural decisions that shape the **revex** project, structured as Architecture Decision Records (ADRs).

---

## Goals
The project should:
- Be easy to understand for beginners.
- Require minimal external dependencies (preferring the Python standard library).
- Work entirely offline.
- Preserve learner work during software updates.
- Allow future content expansion.

## Design Philosophy
- **Prefer:** Explicitness, simple files, discoverable structure, and local ownership of data.
- **Avoid:** Hidden state, unnecessary abstractions, and premature complexity.

---

## ADR 1: Project Naming Conventions
* **Status:** Accepted
* **Context:** The original naming (`review` for the CLI and package name, and `.review` for the state directory) was highly generic. It did not clearly distinguish itself from standard code review, peer review, or spaced repetition cards, and risked collisions with other tools in a developer's path.
* **Decision:** 
  - Rename the project package, CLI command, and imports to `revex` (Short for "Review Exercises").
  - Rename the local application state directory to `.user_data` to clarify that it contains user progress, settings, and local cache.
* **Consequences:** 
  - Provides a distinct, memorable command-line identity (`revex`).
  - Makes user state location explicit and self-documenting.

---

## ADR 2: Separation Between Code and Content
* **Status:** Accepted
* **Context:** Putting course content directly inside application source files makes content updates difficult to ship without risking breaking application logic, and complicates packaging.
* **Decision:** 
  - Strictly isolate application logic inside [src/revex/](../src/revex) from exercise content inside [content/](../content).
* **Consequences:**
  - Content can evolve independently of CLI code.
  - Simplifies distribution and downstream packaging.

---

## ADR 3: Workspace Model
* **Status:** Accepted
* **Context:** If learners edit exercise files directly in the package directory, updating the platform/course material will overwrite their work or trigger git merge conflicts.
* **Decision:** 
  - Establish a separate `/workspace` directory. 
  - Learners never edit files inside `content/`; exercises are copied into the workspace for editing.
* **Consequences:**
  - System updates never overwrite user solutions.
  - Learners can experiment freely in an isolated environment.

---

## ADR 4: Manifest as Source of Truth
* **Status:** Accepted
* **Context:** The application needs a robust, fast way to discover exercises, map their IDs to filesystem paths, and know the release version without scanning the entire disk or parsing python modules at start.
* **Decision:** 
  - Maintain a centralized [manifest.json](../content/manifest.json) in the `content/` folder as the authoritative registry of content.
* **Consequences:**
  - Keeps content discovery separated from content execution/loading.
  - Fast, centralized lookup of exercise attributes (id, group, difficulty, path).

---

## ADR 5: Workspace Synchronization & File Selection
* **Status:** Accepted
* **Context:** Copying the entire exercise directory (including `solution.py` and `validate.py`) directly to the learner's workspace would expose answers locally and clutter their view. We also need a structured directory layout in the workspace.
* **Decision:**
  - The `revex sync` process only copies `exercise.pytxt` (renamed to `<exercise_name>.py`) and the localized problem markdown file (renamed to `README.md`) to the workspace.
  - Workspace folders are organized as `workspace/<group_name>/<padded_id>-<exercise_name>/`.
  - `solution.py` and `validate.py` are strictly excluded from copying.
* **Consequences:**
  - Prevents solution leakage and preserves a clean, focused workspace.
  - Groups exercises by module (e.g. `workspace/primitives/0101-basic_type_hints/basic_type_hints.py`).

---

## ADR 6: Terminal Markdown Rendering
* **Status:** Accepted
* **Context:** Learners need to read exercise descriptions. Having to manually browse markdown files can be friction. 
* **Decision:**
  - Provide a CLI command `revex view <id>` (and `revex view next`) that renders problem descriptions in the console.
  - Integrate with the system-level markdown previewer `glow`. If not installed, provide helper install commands for the host OS.
* **Consequences:**
  - Keeps learners in their terminal/editor workflow.
  - Relies on system `glow` dependency, requiring fallback detection logic.

---

## ADR 7: Progress Storage Format
* **Status:** Accepted
* **Context:** We need a way to track completed exercises. SQLite offers querying power, but adds dependencies and database migration complexity.
* **Decision:**
  - Store progress as JSON in `.user_data/progress.json`.
* **Consequences:**
  - Human-readable, easy to backup, zero-dependency, and extremely simple to serialize.
  - Can transition to SQLite if requirements become significantly complex.

---

## ADR 8: Validation Pipeline Architecture
* **Status:** Accepted
* **Context:** Validation needs to check both syntax rules (e.g., did they write a type hint instead of standard assignments) and actual type accuracy.
* **Decision:**
  - Split validation into a multi-stage pipeline: a main orchestrator runner, an AST structural validator, and a Pyright static type checker.
* **Consequences:**
  - Separation of concerns: each validation step remains focused.

---

## ADR 9: Language Setting Changes Impact
* **Status:** Rejected (Proposed update of existing workspace files)
* **Context:** If a learner changes their language preference, we could update all existing workspace `README.md` files to the new language.
* **Decision:** 
  - Rejected. Changing language settings only affects newly synchronized exercises. Existing workspace `README.md` files are left unmodified.
* **Consequences:**
  - Avoids overwriting any custom notes or annotations the user might have made in their workspace markdown files.

---

## ADR 10: Declarative Validation Specifications
* **Status:** Accepted (Supercedes/Refactors exercise-specific `validate.py` design)
* **Context:** Writing a custom `validate.py` script for every exercise creates excessive boilerplate, especially for simple variable annotation exercises.
* **Decision:**
  - Prefer declarative validation metadata defined within the exercise's `data.json` under a `"validation"` key (e.g. mapping variable names to expected types).
  - Custom `validate.py` files remain supported as an optional escape hatch for complex logic.
* **Consequences:**
  - Drastically reduces boilerplate for curriculum content authors.
  - Centralizes AST verification logic, making it easier to scale and maintain.

---

## ADR 11: Pyright Diagnostics to Hint Translation
* **Status:** Pending
* **Context:** We need to translate Pyright's static analysis output into user-friendly, localized hints.
* **Decision:** 
  - Postponed to evaluate if declarative AST validation in ADR 10 covers the majority of simple cases, rendering complex Pyright mapping logic unnecessary.
