# Architecture

This document records the major design decisions that shaped the project.

---

# Goals

The project should:

- be easy to understand
- require minimal dependencies
- work entirely offline
- preserve learner work during updates
- allow future content expansion

---

# Separation Between Code And Content

The project intentionally separates:

```text
src/review/
```

from

```text
content/
```

Application code lives inside `src/review`.

Course material lives inside `content`.

Benefits:

- cleaner boundaries
- content can evolve independently
- easier future packaging

---

# Workspace Model

Learners never edit files inside `content`.

Instead:

```text
content/
        ↓
workspace/
```

Exercises are copied into the workspace.

Benefits:

- updates never overwrite learner code
- users can experiment freely
- synchronization becomes simpler

---

# Manifest As Source Of Truth

The manifest is the authoritative registry of content.

Responsibilities:

- discover exercises
- expose content version
- map ids to locations

Not responsible for:

- loading files
- progress
- validation

This keeps content discovery separate from content execution.

---

# Content Structure

Each exercise is self-contained.

```text
exercise_id/
    exercise.py
    solution.py
    problem.en.md
    problem.es.md
    data.json
```

Benefits:

- portable exercises
- easier authoring
- straightforward localization

---

# Synchronization Strategy

User work is never overwritten.

Synchronization only adds missing exercises.

Pseudo algorithm:

```python
for exercise in manifest:
    if exercise not in workspace:
        copy(exercise)
```

The workspace is considered learner-owned.

The content directory is considered application-owned.

---

# Progress Storage

Current decision:

```text
JSON
```

instead of

```text
SQLite
```

Reasoning:

- simple schema
- small datasets
- human-readable
- easy backups
- fewer moving parts

SQLite remains an option if future requirements become more complex.

---

# Validation Pipeline

Validation is separated into stages.

```text
runner
    ├── ast_validator
    └── pyright_validator
```

The runner orchestrates validation.

Individual validators remain focused on a single responsibility.

---

# Internationalization

Exercise metadata supports translations.

Content is selected according to:

```text
.review/config.toml
```

Current planned languages:

- English
- Spanish

The design allows additional languages without modifying validation logic.

---

# Design Philosophy

Prefer:

- explicitness
- simple files
- discoverable structure
- local ownership of data

Avoid:

- hidden state
- unnecessary abstractions
- premature complexity
