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
- **[cli/parser.py](./cli/parser.py):** Implements argument parsing using Python's standard `argparse` library. Defines subcommand structures for `setup`, `status`, `sync`, `check`, `set`, and `view`.
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

## 4. System Specifications & ADRs

For detailed specifications, flowcharts, and architectural decision records, consult the developer docs:
- **[docs/architecture.md](./docs/architecture.md):** Records the major design decisions (ADRs).
- **[docs/cli.md](./docs/cli.md):** Visual sequence diagrams and flows for every subcommand lifecycle.
- **[docs/implementation.md](./docs/implementation.md):** Configuration details, markdown previewer utility scripts, and dependency check guides.
- **[docs/implementation_plan.md](./docs/implementation_plan.md):** Ordered roadmap milestones and development phases.
- **[docs/models.md](./docs/models.md):** Entity Relationship Diagrams (ERD) and Classes, Responsibilities, and Collaborators (CRC) indexes.
- **[docs/roadmap.md](./docs/roadmap.md):** Explorer roadmap and future goals.
