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
uv run review setup
```

This creates:

```text
workspace/
.review/
```

---

## Quick Start

List available commands:

```bash
uv run review
```

Check progress:

```bash
uv run review status
```

Validate an exercise:

```bash
uv run review check workspace/variables.assignment/exercise.py
```

Synchronize new content:

```bash
uv run review sync
```

Change language:

```bash
uv run review set --language es
```

---

## Directory Structure

```text
content/
    exercises/
    manifest.json

workspace/
    ...
    
.review/
    progress.json
    config.toml

src/review/
    ...
```

### content/

Canonical course material distributed with the project.

### workspace/

Learner-owned files.

This directory is safe to edit.

### .review/

Application state.

Stores progress, configuration and cache files.

---

## Core Concepts

### Content

Content is versioned and distributed with the project.

Each exercise contains:

```text
exercise.py
solution.py
problem.en.md
problem.es.md
data.json
```

### Workspace

Exercises are copied into the workspace before being solved.

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
