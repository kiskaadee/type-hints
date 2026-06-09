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
src/revex/
```

from

```text
content/
```

Application code lives inside `src/revex`.

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
.user_data/config.toml
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

---

# Additional Architecture Decision Logs (ADL)
Resolution to conflicts and gaps found during the software requirements analysis.

## ADR1- Naming conventions: Accepted
- I've moved the CLI name from `review` to `revex`; 
- I've updated the documentation to reflect the name `.user_data` instead of `.review`

**Rationale**: I think both changes are improvements, for different reasons.

### `review` → `revex`

`review` is descriptive, but it's also extremely generic.

When I first saw:

```text
uv run review check exercise.py
```

I wasn't immediately sure whether it meant:

* code review
* flashcard review
* spaced repetition review
* exercise review

Whereas:

```text
uv run revex check exercise.py
```

has a stronger identity.

It's short, memorable, and unlikely to collide with existing tooling.

The tradeoff is discoverability:

```text
review
```

immediately explains itself.

```text
revex
```

requires reading the README once.

For an open-source educational project, I would probably prefer:

```text
project name: revex
package name: revex
cli command: revex
```

and then explain the meaning in the README.

---

### `.review` → `.user_data`

I think this change is even more important.

When I see:

```text
.review/
```

I have no idea what belongs there.

Could be:

* progress
* logs
* cache
* temporary files
* settings
* validation results

By contrast:

```text
.user_data/
```

communicates intent immediately.

```text
.user_data/
├── config.toml
├── progress.json
└── cache/
```

makes sense without documentation.

One additional consideration is whether we want to distinguish *user-owned state* from *tool-generated cache*

For example:

```text
.user_data/
├── config.toml
└── progress.json

.cache/
```

Because cache can be deleted without consequence.

---

## ADR2 Workspace Sync File Selection: Accepted

**Gap**: 

We have not defined which files from `content/exercises/<id>/` directory are copied 
to `workspace/` during `sync` or `setup`.

**Risk**: 

If the `sync/setup` process copies the entire exercise folder, it will copy  `solution.py`  and  `validate.py`  directly into the learner's workspace. This allows the learner to easily view or copy the solution and exposes validation internals. 

**Decision**: 

During the `revex setup` and `revex sync` flow, the CLI must exclusively copy `exercise.py` and `problem.<lan>.md` (dumped into `README.md`) from the `/content` directory into the `/workspace`. Files containing solutions (`solution.py`) or internal validation logic (`validate.py`) must be strictly excluded from the `workspace/` transfer to prevent answer leakage.

The `data.json` for each exercise contains a two digit group Id and a two digit exercise Id; 
This is used to organize the resulting directory at user's workspace; 

An exercise directory with the default structure: 


```bash
content/
└── exercises/
    └── group_name.exercise_name/
        ├── data.json
        ├── problem.en.md
        ├── problem.es.md
        ├── exercise.py
        └── solution.py
```

Should yield a workspace/ subdirectory like:

```bash
## with Id 0000
group_name
    └── 0000-exercise_name
        ├── exercise_name.py    # editable copy of the unsolved exercise
        └── README.md           # copy of the problem.md file, in the language defined by user settings.
```

Exercises sharing the same group (infered from data.json) will be nested inside the `/workspace/group_name`: 

```text
group_name 
    ├── 0001-exercise_name
    │   ├── exercise_name_1.py
    │   └── README.md
    └── 0002-exercise_name
        ├── exercise_name_2.py
        └── README.md
```

## ADR3 - Displaying and Reading Problem Statements

**Gap**: 

There is no command defined in the CLI to display the problem statement, nor is it clear if learners are expected to read it by opening a file in their editor

**Decision**: 

- During `sync`/`setup`, the CLI should generate a README.md file in the workspace exercise directory. (e.g.  `workspace/primitives/basic_type_hints/README.md`) based on the learner's configured language.


**Additionally**
- Implementing an exercise viewer function: 


`uv run revex view <id>`: `cd` into the `/workspace/<id>/` and outputs the rendered markdown to the console using `glow` 

`uv run revex view next`: `cd` into the `/workspace/<id>/` and outputs the rendered markdown to the console using `glow` ---> same output but replaces next with the next unsolved exercise from progress.


The markdown previewer utility could be something like: 

```python
import subprocess
import sys

def preview_markdown(file_path: str):
    try:
        # Calls the system's glow command
        subprocess.run(["glow", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running glow: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("Error: Glow is not installed on your system.", file=sys.stderr)

if __name__ == "__main__":
    preview_markdown("README.md")

```

If glow isn't found, we should suggest installation:

```python
import platform
import shutil

def is_glow_installed() -> bool:
    """Validates whether the 'glow' binary is present in the system PATH."""
    return shutil.which("glow") is not None


def get_glow_install_instructions() -> str:
    """Detects the host OS (Windows, macOS, or Linux distros) and returns 

    a string with the exact installation instructions.
    """
    system = platform.system().lower()

    # 1. Handle macOS
    if system == "darwin":
        return (
            "💡 Suggested installation for macOS (Homebrew):\n"
            "brew install glow"
        )

    # 2. Handle Windows
    if system == "windows":
        return (
            "💡 Suggested installation for Windows:\n"
            "winget install charmbracelet.glow\n"
            "OR\n"
            "scoop install glow"
        )

    # 3. Handle Linux Distros
    if system == "linux":
        try:
            with open("/etc/os-release") as f:
                os_data = {}
                for line in f:
                    if "=" in line:
                        key, value = line.rstrip().split("=", 1)
                        os_data[key] = value.strip('"')
            
            os_id = os_data.get("ID", "").lower()
            id_like = os_data.get("ID_LIKE", "").lower().split()

        except FileNotFoundError:
            return "❌ Could not determine Linux distribution (/etc/os-release missing)."

        if os_id in ["ubuntu", "debian", "pop", "mint"] or "debian" in id_like or "ubuntu" in id_like:
            return (
                "💡 Suggested installation for Debian/Ubuntu:\n"
                "sudo mkdir -p /etc/apt/keyrings && "
                "curl -fsSL https://charm.sh | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg && "
                'echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://charm.sh * *" | sudo tee /etc/apt/sources.list.d/charm.list && '
                "sudo apt update && sudo apt install glow"
            )

        if os_id in ["fedora", "rhel", "centos", "rocky", "almalinux"] or "fedora" in id_like or "rhel" in id_like:
            return (
                "💡 Suggested installation for Fedora/RHEL:\n"
                "echo -e '[charm]\\nname=Charm\\nbaseurl=https://charm.sh\\nenabled=1\\ndpgcheck=1\\ndpgkey=https://charm.shgpg.key' | sudo tee /etc/yum.repos.d/charm.repo && "
                "sudo dnf install glow"
            )

        if os_id in ["arch", "manjaro"] or "arch" in id_like:
            return "💡 Suggested installation for Arch Linux:\nsudo pacman -S glow"

        if os_id == "alpine":
            return "💡 Suggested installation for Alpine Linux:\nsudo apk add glow"

        # Fallback for unmapped Linux variants
        return (
            "💡 Unrecognized Linux distribution. Suggested universal installation:\n"
            "sudo snap install glow\n"
            "OR\n"
            "flatpak install flathub sh.charm.Glow"
        )

    # 4. Ultimate Fallback (FreeBSD, OpenBSD, etc.)
    return (
        f"❌ Unsupported OS: {platform.system()}.\n"
        "Please install Glow manually from: https://github.com"
    )

```

## ADR4 - Language Setting Changes & Workspace Updates: REJECTED
**Gap**: 

If a user runs  `uv run revex set --language` es  to switch languages, the documentation doesn't specify if existing workspace problem files are updated

**Proposed solution**

Changing the language configuration setting should trigger a partial synchronization process that updates the  README.md  files in the workspace to the newly selected language, while preserving the learner's modifications to  exercise.py

**Decision**: 

Updating language configuration should not trigger a partial synchronization process on existing  `README.md` but only to affect newly downloaded exercises. This prevents the user from losing custom annotations on the Markdown file, if any.

## ADR5 - Dynamic Validation Runner Execution: ACCEPTED 

**Gap**: The validator runner needs to execute valitate(tree) from the exercise's validate.py. Since validate.py resides in `content/` and it's not packaged or static, we need a clear dynamic execution strategy. 

**Decision**: (Refactor) Prefer Declarative Validation Specifications over Exercise-Specific Validators

The initial design proposed that every exercise would contain a dedicated `validate.py` module.

Example:

```text
content/exercises/primitives.basic_type_hints/
├── exercise.py
├── solution.py
├── validate.py
└── data.json
```

The validation runner would dynamically load and execute `validate.py` for each exercise.

While flexible, this approach introduces significant boilerplate. Most early exercises in the curriculum only require verification that specific variables, functions, or classes contain the expected type annotations.

For example, Exercise `0101` only needs to verify:

```python
employee_name -> str
employee_id -> int
hourly_rate -> float
is_full_time -> bool
```

Writing a custom validator for every exercise would duplicate logic and increase maintenance cost.

Therefore, the validation requirements will be declared as data whenever possible. Exercises will define expected annotations inside their metadata.

Example:

```json
{
  "id": "0101",
  "group": "primitives",

  "validation": {
    "annotations": {
      "employee_name": "str",
      "employee_id": "int",
      "job_title": "str",
      "hourly_rate": "float",
      "hours_per_week": "float",
      "age": "int",
      "is_full_time": "bool",
      "completed_orientation": "bool"
    }
  }
}
```

The validation runner will load the specification and execute generic AST-based validation logic.

Pseudo-code:

```python
spec = load_validation_spec(exercise_id)

for variable, expected_type in spec.annotations.items():
    assert_annotation(
        tree,
        variable,
        expected_type,
    )
```

**The advantages**

- Less authoring effort: Adding a new exercise typically requires editing metadata rather than writing Python validation code.

- Consistent validation: All exercises use the same validation engine and error reporting mechanisms.

- Reduced complexity: The runner no longer needs to dynamically import and execute exercise-specific validators for common cases.

- Easier localization: Hints and validation rules remain data-driven and can be stored alongside exercise metadata.

- Better scalability: Large numbers of exercises can be added with minimal implementation effort.

**Disadvantages**

- Reduced flexibility: Some validation scenarios cannot be easily represented as data.

Examples:
* complex AST patterns
* custom code structure requirements
* FastAPI dependency injection exercises
* advanced generic typing exercises

### Validator schema growth

As new exercise types are introduced, the validation schema may become more complex.
For example:

```json
{
  "validation": {
    "functions": {},
    "typed_dicts": {},
    "dataclasses": {},
    "pydantic_models": {}
  }
}
```

### Future Extension Point

Exercise-specific validators remain an optional escape hatch.

Structure:

```text
content/exercises/<exercise>/
├── exercise.py
├── solution.py
├── data.json
└── validate.py   # optional
```

Validation strategy:

```python
if custom_validator_exists():
    run_custom_validator()
else:
    run_generic_validator()
```

Most exercises are expected to use declarative validation.

Custom validators should be reserved for advanced exercises where validation logic cannot be expressed through metadata.

**Rationale**:

The curriculum is primarily focused on learning type annotations through repetition and pattern recognition.

For the majority of exercises, validation requirements are data rather than behavior.

Treating validation as declarative metadata reduces boilerplate, simplifies exercise creation, and keeps the validation engine centralized while preserving the ability to introduce custom validation when genuinely required.


## ADR6 - Pyright Diagnostic Mapping to Localized Hints: PENDING

The architecture outlines  pyright_validator  as translating diagnostics into error codes, but doesn't specify how standard Pyright output maps to localized errors in `data.json`. 

Decision: Pending: 
Evaluating if this is still a problem after refactoring the validation model (ADR5)

---
# More suggestions

## Proposed Data Schemas

### A. Progress File Schema ( .user_data/progress.json )

tracking completion status, timestamps, and attempts for richer user metrics: Accepted

```json
{
  "completed_exercises": {
    "0101": {
      "completed": true,
      "completed_at": "2026-06-08T19:15:20-05:00",
      "attempts": 3
    }
  }
}
```


### B. Config File Schema (.user_data/config.toml)

```toml
[settings]
language = "en"
allow_hints = false
```
