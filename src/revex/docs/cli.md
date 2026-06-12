# CLI Workflow & Interaction Flows

This document details the command execution flows, terminal rendering behaviors, and sequence patterns of the **revex** CLI commands.

---

## 1. Setup Flow (`revex init`)

This command initializes a learner's environment. It is idempotent; if run multiple times, it will only create files/folders if they do not exist.

### Sequence Diagram
```mermaid
sequenceDiagram
    actor Learner
    participant CLI as revex CLI
    participant FS as Filesystem
    
    Learner->>CLI: run "revex init"
    CLI->>FS: Check for /workspace and /.user_data
    alt Folders do not exist
        CLI->>FS: Create /workspace directory
        CLI->>FS: Create /.user_data directory
        CLI->>FS: Generate config.toml with default Settings
        CLI->>FS: Generate empty progress.json
    end
    CLI->>CLI: Invoke Sync Flow
    CLI->>Learner: Print initialization success message
```

---

## 2. Synchronization Flow (`revex sync`)

This command keeps the user's workspace aligned with the central content catalog. It strictly respects the workspace model guarantees, ensuring existing user solutions are never overwritten.

### Sync Selection and File Mapping Logic

```mermaid
flowchart TD
    Start[Load manifest.json] --> Loop[For each exercise in manifest]
    Loop --> Check{Exists in /workspace?}
    Check -- Yes --> Skip[Skip copying exercise.pytxt - preserve user solution]
    Check -- No --> Copy[Copy files]
    Copy --> CreateDir[Create workspace/group_name/padded_id-exercise_name/]
    CreateDir --> CopyCode[Copy content/.../exercise.pytxt as <exercise_name>.py]
    CreateDir --> CopyLang[Copy content/.../problem.lang.md as README.md based on config]
    Skip --> Next[Process next exercise]
    CopyLang --> Next
```

---

## 3. Validation Flow (`revex check`)

This command evaluates the learner's solution, orchestrating the declarative AST validation and Pyright static type check.

### Flowchart
```mermaid
flowchart TD
    A[Learner runs revex check PATH] --> B[Infer Exercise ID from Path]
    B --> C[Load exercise data.json]
    C --> D[Parse learner's exercise file into AST]
    
    D --> E{Has custom validate.py?}
    E -- Yes --> F[Execute custom validator]
    E -- No --> G[Execute generic AST validator using declarative spec]
    
    F --> H{AST check passes?}
    G --> H
    
    H -- No --> ErrAST[Look up error_code in data.json & Print hint]
    H -- Yes --> Pyright[Run Pyright on solution file]
    
    Pyright --> PassPyright{Pyright passes?}
    PassPyright -- No --> ErrPyright[Print type checker diagnostics]
    PassPyright -- Yes --> UpdateProg[Update progress.json]
    
    UpdateProg --> Success[Display completion success message]
```

---

## 4. Problem Viewer Flow (`revex view`)

This command outputs the formatted markdown description to the console.

### Sequence Diagram
```mermaid
sequenceDiagram
    actor Learner
    participant CLI as revex CLI
    participant Util as is_glow_installed() Helper
    
    alt View Next
        Learner->>CLI: run "revex view next"
        CLI->>CLI: Find first incomplete exercise ID in progress.json
    else View Specific ID
        Learner->>CLI: run "revex view <id>"
        CLI->>CLI: Locate exercise in manifest
    end
    
    CLI->>Util: Check if "glow" CLI is in system PATH
    alt Glow is installed
        CLI->>CLI: subprocess.run(["glow", "README.md"])
        CLI->>Learner: Render formatted output to terminal
    else Glow is missing
        CLI->>CLI: Call get_glow_install_instructions()
        CLI->>Learner: Output install command suggestions and fallback text
    end
    CLI->>Learner: Print navigation tip (workspace path and cd command)
```
