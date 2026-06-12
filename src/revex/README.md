# Revex CLI Developer Guide

This directory contains the source code for the **revex** CLI command-line interface. It is structured to maintain a strict separation of concerns between user interaction (presentation) and type-checking logic (domain services).

---

## 1. CLI Code Directory Layout

The codebase is divided into two primary sub-packages:

```text
src/revex/
├── main.py              # Lightweight bootloader/entrypoint
│
├── cli/                 # Presentation Layer
│   ├── __init__.py
│   ├── parser.py        # Argparse subcommand and options definition
│   └── commands.py      # Console rendering, stdout/stderr, and flow routing
│
├── core/                # Bounded Domain Layer (Unaware of CLI terminal output)
│   ├── models/          # Pydantic schemas (Config, Progress, ExerciseBase, errors)
│   ├── services/        # Logic services (Workspace Setup, Sync, Content Loaders)
│   └── validators/      # Validation Runner, AST checker, and Pyright wrapper
│
└── docs/                # System Architecture, CLI Flows, and Developer Roadmaps
```

---

## 2. Main Components and Roles

### Presentation Layer (`cli/`)
- **[main.py](./main.py):** The lightweight main execution script. It initializes [create_parser](./cli/parser.py) to resolve subcommands and redirects execution parameters to commands handlers.
- **[cli/parser.py](./cli/parser.py):** Implements argument parsing using Python's standard `argparse` library. Defines subcommand structures for `init`, `status`, `sync`, `check`, `set`, and `view`.
- **[cli/commands.py](./cli/commands.py):** Handles terminal outputs, printing format blocks, and user feedback decorators (e.g. `glow` subprocesses). Translates data models returned by domain services into user-facing console text.

### Core Bounded Domain Layer (`core/`)
- **[core/models/](./core/models/):** Defines Pydantic validation models for config TOMLs, progress logs, exercise catalog records, and error diagnostics.
- **[core/services/](./core/core/services/):** Contains pure, side-effect-isolated Python logic for directory initialization, copying exercise templates, and reading progress records.
- **[core/validators/](./core/core/validators/):** Coordinates type-hints checking:
  - `ast_validator.py` checks code structure rules defined in the exercise's `data.json`.
  - `pyright_validator.py` executes Pyright diagnostics as a background subprocess.
  - `runner.py` orchestrates execution and updates completion status.

---

## 3. Developer Workflow

### Installation
To install the package locally in editable mode (so your code changes take effect immediately):
```bash
uv sync
```

### Type Checking
Run Pyright type checking across the CLI source codebase:
```bash
uv run pyright
```

### Linting and Formatting
Check formatting and apply ruff style rule checks:
```bash
uv run ruff check src
```

---

## 4. Type Safety & Pyright Cookbook

During development under Pyright's strict rules, we've established several patterns to satisfy type safety without adding runtime overhead:

### Pattern 1: Annotating Dynamically Parsed Namespace Objects
* **Problem**: Subclassing `argparse.Namespace` with class-level type annotations triggers Pyright's warning: `Instance variable "..." is not initialized in the class body or __init__ method`.
* **Solution**: Use `typing.Protocol` to declare the structure statically, and `typing.cast` to cast the return value of `parse_args()`.
  ```python
  from typing import Protocol, cast

  class CLIArgs(Protocol):
      command: str
      target: str | None

  args = cast(CLIArgs, parser.parse_args())
  ```
  * **Why**: Protocols are purely static interfaces, so they do not require variable initialization and introduce zero runtime overhead.

### Pattern 2: Enforcing Pydantic Field Validation on In-Place Updates
* **Problem**: Reassigning fields directly on a Pydantic model instance (e.g. `config.settings.language = "es"`) does not automatically trigger Pydantic validators.
* **Solution**: Use `.model_copy(update=...)` followed by `.model_validate(...)` to validate the new dictionary values before saving.
  ```python
  updated_settings = config.settings.model_copy(update=settings_updates)
  config.settings = Settings.model_validate(updated_settings.model_dump())
  ```
  * **Why**: This triggers custom `@field_validator` and type-checking rules at the boundary before persisting changes.

### Pattern 3: Strict Subclassing and Class Contracts
* **Problem**: If a class with constructor annotations is not marked as `@final`, Pyright requires class-level type annotations or an explicit constructor initialization to protect against subclass overrides.
* **Solution**: Declare the type of all instance attributes at the class level or initialize them fully in `__init__`.

### Pattern 4: Safe Type Narrowing with Union Types
* **Problem**: Passing a union type like `str | None` to a function expecting `str` raises a type mismatch.
* **Solution**: Use explicit type guards (e.g. `if args.target is not None`) to narrow the type down to `str`.

---

## 5. System Specifications & ADRs

For detailed specifications, flowcharts, and architectural decision records, consult the developer docs:
- **[architecture.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/architecture.md):** Records the major design decisions (ADRs).
- **[authoring_guide.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/authoring_guide.md):** Step-by-step instructions for creating and registering new exercises.
- **[cli.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/cli.md):** Visual sequence diagrams and flows for every subcommand lifecycle.
- **[implementation.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/implementation.md):** Configuration details, markdown previewer utility scripts, and dependency check guides.
- **[implementation_plan.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/implementation_plan.md):** Ordered roadmap milestones and development phases.
- **[models.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/models.md):** Entity Relationship Diagrams (ERD) and CRC indexes.
- **[roadmap.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/roadmap.md):** Explorer roadmap and future goals.
