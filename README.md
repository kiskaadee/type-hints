# Type Hints

A command-line learning platform for practicing Python type hints through
small exercises, automated validation, and progress tracking.

The project is designed around a simple idea:

> Learn by editing code locally and receiving immediate feedback.

Exercises are distributed as content packages and copied into a personal
workspace where learners can freely modify them without affecting the
canonical exercise sources.

---

## Features

- Structured learning path
- Progressive exercises grouped by topic
- Automated validation
- Progress tracking
- Local-first workflow
- Multi-language content support
- Content synchronization without overwriting learner work

---

## Installation

### Prerequisites

For the best learning experience, we recommend having the following tools installed:

- **[uv](https://github.com/astral-sh/uv)** — A fast Python package installer and resolver.
- **[glow](https://github.com/charmbracelet/glow)** — A terminal markdown reader for beautiful exercise descriptions.
- **[direnv](https://direnv.net/)** (recommended) — To automatically load the Python virtual environment upon entering the project directory.

### Setup

Clone the repository:

```bash
git clone https://github.com/kiskaadee/type-hints.git
cd type-hints
```

Install dependencies:

```bash
uv sync
```

Initialize your workspace:

```bash
uv run revex init
```

This creates:

```text
workspace/
.user_data/
```

---

## Quick Start

List available commands:

```bash
uv run revex
```

Check progress:

```bash
uv run revex status
```

Validate an exercise:

```bash
uv run revex check workspace/primitives/0101-basic_type_hints/basic_type_hints.py
```

Synchronize new content:

```bash
uv run revex sync
```

Configure settings:

```bash
# Change language preference (en or es)
uv run revex set --language es

# Toggle static hints on error
uv run revex set --allow-hints false

# Toggle glow terminal markdown styling
uv run revex set --allow-glow true
```

---

## Directory Structure

```text
content/
    exercises/
    manifest.json

workspace/
    ...
    
.user_data/
    progress.json
    config.toml

src/revex/
    ...
```

### content/

Canonical course material distributed with the project.

### workspace/

Learner-owned files.

This directory is safe to edit.

### .user_data/

Application state.
Git-ignored. Not affected by `revex sync` or `revex init` actions.
Stores user progress, local configuration and cache files.

---

## Core Concepts

### Content

Content is versioned and distributed with the project.

Each exercise contains:

```text
topic_name.exercise_name
    ├── assets/         # resources like images, pdf documents or other files when needed
    ├── data.json       # exercise metadata and validation rules
    ├── exercise.pytxt  # python template with deliberate errors or missing type hints to be solved
    ├── problem.en.md   # markdown file expressing the problem description and references.
    ├── problem.es.md   # Spanish translation. 
    ├── solution.py     # solved python script with proper type annotations
    └── validate.py     # (Optional) custom validator script (escape hatch)
```



### /workspace
Git-ignored. Not affected by `revex sync` or `revex init` actions.
Exercises are copied into the workspace before being solved.

An exercise-content directory with the aforemention structure 
should yield a directory with the following elements: 

```text
group_name
    └── 0000-exercise_name
        ├── exercise_name.py    # editable copy of the unsolved exercise
        └── README.md           # copy of the problem.md file, using settings-defined language
```

While the `/content` directory isn't nested, exercises sharing the same group will be nested inside the same group directory at `/workspace`: 

```text
topic_name
    ├── 0001-exercise_name_1
    │   ├── exercise_name_1.py
    │   └── README.md
    └── 0002-exercise_name_2
        ├── exercise_name_2.py
        └── README.md
```

This ensures updates never overwrite learner code.

### Manifest

The manifest is the authoritative catalog of available content.

It answers:

- What exercises exist?
- Where are they located?
- What version of content is installed?

### Progress

Progress is stored independently from content so updates can safely
introduce new exercises.

---

## Developer Documentation

- [architecture.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/architecture.md)
- [authoring_guide.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/authoring_guide.md)
- [roadmap.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/roadmap.md)
- [cli.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/cli.md)
- [implementation.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/implementation.md)
- [implementation_plan.md](file:///home/kiskaadee/Projects/type-hints/src/revex/docs/implementation_plan.md)

---

## Project Status

Core features are fully functional. Milestones 1 through 5 are complete, including workspace initialization (`revex init`), catalog synchronization (`revex sync`), terminal markdown rendering (with optional `glow` support), static AST and Pyright validation (`revex check`), settings management (`revex set`), and progress statistics reporting (`revex status`).
