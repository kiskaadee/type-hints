# Exercise Authoring Guide

This guide details the step-by-step process for authoring and registering new exercises for the **revex** learning platform.

---

## 1. Exercise File Structure

Each exercise is contained within its own directory under `content/exercises/`. The directory name must follow the naming convention `<group>.<exercise_name>` (e.g. `primitives.basic_type_hints`).

An exercise folder contains the following files:

```text
content/exercises/group_name.exercise_name/
├── data.json         # Exercise metadata, AST validation rules, and hints
├── exercise.pytxt    # Python code template containing the exercise for the student
├── problem.en.md     # Problem description in English (default)
├── problem.es.md     # (Optional) Problem description in Spanish
├── solution.py       # Reference solution that passes all validations
└── assets/           # (Optional) Images, diagrams, or other static assets
```

---

## 2. Step-by-Step Creation Flow

### Step 1: Register the Exercise in the Manifest
Before creating any files, open the main catalog manifest at [content/manifest.json](file:///home/kiskaadee/Projects/type-hints/content/manifest.json) and add an entry under `"exercises"`:

```json
{
  "id": "0102",
  "path": "content/exercises/primitives.variable_reassignment",
  "group": "primitives",
  "difficulty": "beginner"
}
```

> [!IMPORTANT]
> * The `id` must be a unique, exactly **4-digit string** (e.g., `"0102"`).
> * The `group` must align with the topic (e.g., `primitives`, `collections`, `classes`).
> * The `difficulty` must be one of `"beginner"`, `"intermediate"`, or `"advanced"`.

---

### Step 2: Create the Exercise Metadata (`data.json`)
Create `data.json` inside your exercise folder. This file configures the static AST checks and localizations.

```json
{
  "id": "0102",
  "group": "primitives",
  "difficulty": "beginner",
  "tags": ["reassignment", "variable-annotations"],
  "validation": {
    "annotations": {
      "counter": {
        "type": "int",
        "error_code": "PRIMITIVE_REASSIGN_001"
      }
    }
  },
  "translations": {
    "en": {
      "title": "Variable Reassignment",
      "hints": {
        "error_codes": {
          "PRIMITIVE_REASSIGN_001": "The 'counter' variable should be typed as a whole number. Try using the 'int' type hint."
        }
      }
    },
    "es": {
      "title": "Reasignación de Variables",
      "hints": {
        "error_codes": {
          "PRIMITIVE_REASSIGN_001": "La variable 'counter' debe ser de tipo número entero. Intente utilizar el type hint 'int'."
        }
      }
    }
  }
}
```

#### How validation rules match:
* Under `validation.annotations`, each key represents the name of a variable that must be annotated.
* `type` defines the exact text of the expected type hint (e.g., `"int"`, `"list[str]"`).
* `error_code` is a unique diagnostic code. This code maps directly to the localized messages in `translations.<lang>.hints.error_codes`.

---

### Step 3: Write the Code Template (`exercise.pytxt`)
The `exercise.pytxt` file is the template copied to the learner's workspace when they synchronize. It should contain the code skeleton, comments, and deliberate errors or missing annotations for the learner to solve.

```python
# TODO: Annotate 'counter' as an integer
counter = 10

# Do not modify the code below this line
counter = counter + 5
print(f"Count is: {counter}")
```

---

### Step 4: Write the Reference Solution (`solution.py`)
Create a `solution.py` file containing the correct answer. The test suite and validators use this to verify that a fully solved exercise passes all structural and type-checking validations.

```python
# TODO: Annotate 'counter' as an integer
counter: int = 10

# Do not modify the code below this line
counter = counter + 5
print(f"Count is: {counter}")
```

---

### Step 5: Write the Problem Description (`problem.en.md`)
Write a markdown file describing the task, concepts, and references. This is displayed when the learner runs `revex view <id>`.

```markdown
# Variable Reassignment

In this exercise, you'll learn how to annotate a simple integer variable.

## Task
1. Look for the variable named `counter` at the top of the file.
2. Annotate it using Python's primitive `int` type hint.

## References
* [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
```

---

## 3. Testing Your New Exercise

Once all files are written, follow this manual testing flow to verify the exercise functions properly:

1. **Synchronize the workspace**:
   Run the sync command to pull your new exercise into the local workspace:
   ```bash
   uv run revex sync
   ```
   Verify that `workspace/primitives/0102-variable_reassignment/` is successfully created with your template and `README.md`.

2. **Verify Failure Mode**:
   Run the validator check on the unsolved template:
   ```bash
   uv run revex check workspace/primitives/0102-variable_reassignment/variable_reassignment.py
   ```
   Confirm that validation fails and outputs your custom error code and translation hint (e.g., `PRIMITIVE_REASSIGN_001`).

3. **Verify Success Mode**:
   Copy the contents of `solution.py` into your active workspace file, then run the check again:
   ```bash
   uv run revex check workspace/primitives/0102-variable_reassignment/variable_reassignment.py
   ```
   Confirm that the validator passes cleanly with a success message!
