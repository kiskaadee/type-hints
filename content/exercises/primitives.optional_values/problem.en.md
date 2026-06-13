# Exercise 0102 — Optional Values & Type Guards

## Goal

Learn how to annotate variables that can be either a specific type or `None` (representing missing or optional values), and how to use type guards (narrowing) to satisfy strict type-checking checks.

## Problem Statement

In our customer support ticket system, some fields are required when a ticket is created (like `ticket_id` and `customer_name`), but other fields (like `assigned_agent` and `resolution_notes`) start out as empty (`None`) and are only populated later.

Under strict type checking mode, if a variable is annotated as `str | None`, it cannot be passed directly to a function that expects a strict `str`. You must verify that the variable is not `None` before using it. This is called **Type Narrowing** or a **Type Guard**.

1. Replace the `"???"` type annotations for `assigned_agent` and `resolution_notes` with the correct union type representing a string or `None`.
2. Wrap the call to `close_ticket` in an `if` statement checking that `assigned_agent` is not `None`.

Example:

```python
assigned_agent: "???" = None
```

should become:

```python
assigned_agent: str | None = None
```

And:

```python
close_ticket(assigned_agent)
```

should become:

```python
if assigned_agent is not None:
    close_ticket(assigned_agent)
```

## Success Criteria

The exercise passes when:
- Both `assigned_agent` and `resolution_notes` are annotated as `str | None`.
- The code passes strict Pyright type checking without any errors.
