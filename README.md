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
uv run revex setup
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
uv run revex check workspace/variables.assignment/exercise.py
```

Synchronize new content:

```bash
uv run revex sync
```

Change language:

```bash
uv run revex set --language es
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
Git-ignored. Not affected by `revex sync` or `revex setup` actions.
Stores user progress, local configuration and cache files.

---

## Core Concepts

### Content

Content is versioned and distributed with the project.

Each exercise contains:

```text
topic_name.exercise_name
    ├── assets/         # resources like like images, pdf documents or other files when needed
    ├── data.json       # exercise metadata  
    ├── exercise.py     # A python script with deliberate errors or missing type hints to be solved
    ├── problem.en.md   # A markdown file expressing the problem description and references.
    ├── problem.es.md   # A Spanish translation. 
    ├── solution.py     # The solved python script with proper type annotations
    └── validate.py     # A python test performing the AST-based validation of the user's solution.
```



### /workspace
Git-ignored. Not affected by `revex sync` or `revex setup` actions.
Exercises are copied into the workspace before being solved.

An exercise-content directory with the aforemention structure 
should yield a directory with the following elements: 

```text
group_name
    └── exercise_name
        ├── exercise_name.py    # editable copy of the unsolved exercise
        └── README.md           # copy of the problem.md file, in the language defined by user settings.
```

While the `/content` directory isn't nested, exercises sharing the same group will be nested inside the same group directory at `/workspace`: 

```text
topic_name
    ├── exercise_name_1
    │   ├── exercise_name_1.py
    │   └── README.md
    └── exercise_name_2
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

## Documentation

- docs/architecture.md
- docs/roadmap.md

---

## Project Status

Early development.

The architecture is being established before implementation begins.
