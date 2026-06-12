# Course Outline

Exercises are designed to challenge the learner to implement type annotations with increasing levels of complexity, building active research skills, muscle memory, and strict type-safety habits. The focus is strictly on type annotations in different use cases, rather than teaching other language features.

---

## Group 01 — Primitives (`primitives`)

All exercises in this group have the ID `01xx`.

### Exercise 0101: Basic Variable Annotations
* **Hartman Taxonomy Level**: Familiarity & Comprehension
* **Topics**: `str`, `int`, `float`, `bool`
* **Scenario**: Employee onboarding profile.
* **Practice**: Filling in `???` blanks with simple primitive type hints.
  ```python
  employee_name: str
  employee_id: int
  hourly_rate: float
  is_full_time: bool
  ```

### Exercise 0102: Optional Values & Type Narrowing
* **Hartman Taxonomy Level**: Conscious Effort & Conscious Action
* **Topics**: `str | None`, `Optional[str]`, and type narrowing with `is not None` guards.
* **Scenario**: Customer support ticket.
* **Practice**: Declaring nullable fields and using type guards to satisfy strict parameters.
  ```python
  assigned_agent: str | None = None
  
  # Type guard required under strict check
  if assigned_agent is not None:
      process_agent(assigned_agent)
  ```

---

## Group 02 — Collections (`collections`)

All exercises in this group have the ID `02xx`.

### Exercise 0201: Homogeneous Collections
* **Hartman Taxonomy Level**: Familiarity & Comprehension
* **Topics**: `list[str]`, `set[str]`, `dict[str, str]`, and `tuple[float, float]`
* **Scenario**: Team roster and coordinate tracking.
* **Practice**: Annotating collection types containing single type parameters.

### Exercise 0202: Complex Nested Collections
* **Hartman Taxonomy Level**: Conscious Effort & Conscious Action
* **Topics**: `list[dict[str, str]]`, `dict[str, list[int]]`
* **Scenario**: Warehouse inventory system.
* **Practice**: Building complex nested annotations for hierarchical structures.

---

## Group 03 — Functions (`functions`)

All exercises in this group have the ID `03xx`.

### Exercise 0301: Function Parameters and Return Types
* **Hartman Taxonomy Level**: Comprehension
* **Topics**: Parameter type annotations and function return types (`-> float`, `-> None`).
* **Scenario**: Price calculator with tax application.
* **Practice**: Writing basic function signatures.

### Exercise 0302: Callable Parameters & Overloads
* **Hartman Taxonomy Level**: Conscious Action & Proficiency
* **Topics**: `Callable[[int], str]`, `@overload` decorator.
* **Scenario**: Event handler registry and polymorphic utility functions.
* **Practice**: Typing functions that accept other functions, and specifying multiple call signatures.

---

## Group 04 — Structured Data (`structures`)

All exercises in this group have the ID `04xx`.

### Exercise 0401: Type Aliases
* **Hartman Taxonomy Level**: Comprehension
* **Topics**: `type UserId = int`, `type Email = str` (using PEP 695 type statement or `TypeAlias` fallback).
* **Scenario**: User management service.
* **Practice**: Creating domain-specific type aliases to make code more readable.

### Exercise 0402: Enums and Literal Types
* **Hartman Taxonomy Level**: Conscious Effort
* **Topics**: `enum.Enum`, `Literal["pending", "shipped"]`
* **Scenario**: E-commerce order status workflow.
* **Practice**: Limiting values to exact literal strings or Enum choices.

### Exercise 0403: TypedDict and Dataclasses
* **Hartman Taxonomy Level**: Conscious Action
* **Topics**: `typing.TypedDict`, `@dataclass`, handling uninitialized field warnings under strict mode.
* **Scenario**: Configuring a strict database model representation.
* **Practice**: Choosing between dict-like structures and dataclasses, resolving class contract initialization errors.

### Exercise 0404: Casting Parsed JSON-like Objects
* **Hartman Taxonomy Level**: Conscious Action & Proficiency
* **Topics**: `json.loads()`, `typing.cast`, `Any` boundary resolution.
* **Scenario**: Parsing raw JSON API payloads into typed dictionaries.
* **Practice**: Preventing `Any` propagation by explicitly casting dynamic inputs.

---

## Group 05 — Interfaces & Protocols (`protocols`)

All exercises in this group have the ID `05xx`.

### Exercise 0501: Structural Typing with Protocols
* **Hartman Taxonomy Level**: Conscious Action & Proficiency
* **Topics**: `typing.Protocol`, interface segregation.
* **Scenario**: Mocking external services (e.g. database connections, API clients) for unit tests without inheritance.
* **Practice**: Writing runtime-free structural contracts to type-check duck-typed components.

### Exercise 0502: Generics and Type Variables
* **Hartman Taxonomy Level**: Proficient
* **Topics**: `Generic[T]`, `TypeVar("T")`
* **Scenario**: Custom Repository or Cache class.
* **Practice**: Writing re-usable classes and helper functions that preserve the internal types of their collections.

---

## Group 06 — Data Validation & Pydantic (`pydantic`)

All exercises in this group have the ID `06xx`.

### Exercise 0601: Simple Pydantic Models
* **Hartman Taxonomy Level**: Comprehension
* **Topics**: `pydantic.BaseModel`, type validation.
* **Scenario**: User registration payload.
* **Practice**: Building schema contracts for incoming payloads.

### Exercise 0602: Nested Models & Boundary Validation
* **Hartman Taxonomy Level**: Conscious Action & Proficiency
* **Topics**: Nested `BaseModel` attributes, updating models via `.model_copy(update=...)` + `.model_validate()`.
* **Scenario**: Complex transaction ledger settings update.
* **Practice**: Modifying Pydantic models in-place while ensuring validation rules are executed.

### Exercise 0603: Generic Pydantic Models
* **Hartman Taxonomy Level**: Proficient
* **Topics**: `pydantic.generics.GenericModel` (or Pydantic v2 Generic `BaseModel`).
* **Scenario**: Standardized envelope response `ApiResponse[T]`.
* **Practice**: Wrapping data payloads in generic structures.

---

## Group 07 — Web Framework Integration (`fastapi`)

All exercises in this group have the ID `07xx`.

### Exercise 0701: FastAPI Request and Response Typing
* **Hartman Taxonomy Level**: Conscious Action
* **Topics**: `response_model`, typing query/path parameters.
* **Scenario**: Restful API endpoints for resources.
* **Practice**: Enforcing validation at the HTTP entry and exit points.

### Exercise 0702: Dependency Injection Typing
* **Hartman Taxonomy Level**: Proficient
* **Topics**: `typing.Annotated`, `fastapi.Depends`.
* **Scenario**: Injecting database sessions or authenticated users.
* **Practice**: Creating modular, type-safe dependency declarations.

---

## Group 08 — Real Project Review (`capstone`)

All exercises in this group have the ID `08xx`.

### Exercise 0801: Capstone Project
* **Hartman Taxonomy Level**: Unconscious Competence
* **Topics**: Complex refactoring, full codebase type restoration.
* **Scenario**: Restoring type hints to a complete, broken, and untyped FastAPI service under strict Pyright configurations.
* **Practice**: Synthesizing all previous groups (primitives, optionals, protocols, generics, Pydantic, and FastAPI injection) to make the capstone codebase pass checks cleanly.
