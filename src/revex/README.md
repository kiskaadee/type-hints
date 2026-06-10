# RevEx (revex) CLI

A command-line tool for practicing Python type hints through guided exercises.

The repository contains the official exercise catalog and validation logic.

Your work, configuration, and progress are stored separately, allowing course content to be updated without overwriting your solutions.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd type-hints
```

Install dependencies:

```bash
uv sync
```

Initialize your local workspace:

```bash
uv run revex setup
```

This creates:

```text
workspace/
.user_data/
```

---

## Directory Layout

After setup:

```text
type-hints/
│
├── workspace/
│   ├── primitives/
│   │   └── 0101-basic_type_hints/
│   │       ├── basic_type_hints.py
│   │       └── README.md
│   └── ...
│
├── .user_data/
│   ├── config.toml
│   ├── progress.json
│   └── cache/
│
├── content/
│   └── ...
│
└── src/
```

### workspace/

Contains learner-facing exercises.

You are expected to modify files inside this directory.

### .user_data/

Contains local application state.

Files in this directory should not be edited manually.

### content/

Contains bundled course content distributed with the application.

These files are considered read-only.

---

# Commands

## Setup

Initialize the learner environment.

```bash
uv run revex setup
```

Creates the workspace and application state directories.

---

## Status

Display current progress.

```bash
uv run revex status
```

Example:

```text
Your Progress: 12/30

Primitives      ✓
Collections    ✓
Functions      ◐
Union          ✗
```

---

## Check

Validate an exercise.

Usage: 
```bash
# check current
cd workspace/primitives/basic_type_hints
uv run revex check 
```

```bash
# check by group
cd workspace/primitives/
uv run revex check 
```

```bash
# check by id
uv run revex check <id> 
```

```bash
# check at path
uv run revex check workspace/primitives/basic_type_hints 
```

Validation may include:

**Lazy evaluation**:  if the `workspace's`  is equal to solution.py

* AST-based structural checks
* Static type analysis
* Exercise-specific rules


Successful validation updates progress automatically.

---

## Settings

View or update user preferences.

```bash
uv run revex set --language en
```

Supported languages:

* en
* es

---

## Sync

Synchronize your workspace with the latest available course content.

```bash
uv run revex sync
```

The sync process:

* adds newly released exercises
* updates workspace metadata
* preserves existing learner solutions

Sync never overwrites files modified by the learner.

---

# Updating

Pull the latest repository changes:

```bash
git pull
```

Then synchronize content:

```bash
uv run revex sync
```

This updates your workspace without losing progress.

---

# Exercise Structure

Each exercise is distributed as a self-contained content package:

```text
content/
└── exercises/
    └── group.name/
        ├── data.json
        ├── problem.en.md
        ├── problem.es.md
        ├── exercise.pytxt
        ├── solution.py
        └── validate.py   # (Optional) custom validator script (escape hatch)
```

### data.json

Metadata:

* identifier
* difficulty
* tags
* localized hints

### problem.<language>.md

Exercise statement and learning material.

### exercise.pytxt

Starter template code.

### solution.py

Reference implementation used internally.

---

# Design Goals

* Learner work is never overwritten.
* Course content can evolve independently of user progress.
* Exercises are fully versioned.
* All validation logic remains local and transparent.
* Content and application logic remain separate.
