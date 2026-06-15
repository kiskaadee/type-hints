# Course Outline

Exercises are designed to challenge the learner to implement type annotations with increasing levels of complexity, building active research skills, muscle memory, and strict type-safety habits. The focus is on type annotations and static check resolution in different use cases, rather than teaching general python features.

Following a "Pyright Detective" philosophy, early exercises introduce basic syntax, while later exercises present functional code with strict Pyright errors that the learner must resolve without modifying runtime behavior.

---

## Group 01 — Primitives & Optionals (`primitives`)

All exercises in this group have the ID `01xx`.

### Exercise 0101: Basic Variable Annotations
* **Topics**: `str`, `int`, `float`, `bool`
* **Scenario**: Employee onboarding profile.
* **Practice**: Filling in `???` blanks with simple primitive type hints.

### Exercise 0102: Optional Values & Simple Narrowing
* **Topics**: `str | None` / `Optional[str]`, type narrowing with `is not None` checks.
* **Scenario**: Customer support ticket.
* **Practice**: Declaring nullable fields and using type guards to satisfy strict parameters.

---

## Group 02 — Basic & Nested Collections (`collections`)

All exercises in this group have the ID `02xx`.

### Exercise 0201: Homogeneous Collections
* **Topics**: `list[str]`, `set[str]`, `dict[str, int]`, and `tuple[float, float]`
* **Scenario**: Team roster and coordinate tracking.
* **Practice**: Annotating collection types containing single type parameters.

### Exercise 0202: Complex Nested Collections
* **Topics**: `list[dict[str, list[int]]]`, `dict[str, list[dict[str, str]]]`
* **Scenario**: Warehouse inventory system.
* **Practice**: Building complex nested annotations for hierarchical structures.

---

## Group 03 — Unions & Narrowing (`narrowing`)

All exercises in this group have the ID `03xx`.

### Exercise 0301: Union Types
* **Topics**: `str | int`, parameter type widening, return path type validation.
* **Scenario**: Universal parser for user IDs or codes.
* **Practice**: Specifying multiple allowed types for function inputs and outputs.

### Exercise 0302: Standard Narrowing
* **Topics**: `isinstance()`, `assert`, structural checks (`hasattr`).
* **Scenario**: Event payload processor.
* **Practice**: Using runtime checks to convince Pyright of specific types within block scopes.

### Exercise 0303: Custom Type Guards
* **Topics**: `typing.TypeGuard`, `typing.TypeIs`
* **Scenario**: Custom JSON parser or domain-specific validator.
* **Practice**: Writing functions that act as custom type narrowing predicates.

---

## Group 04 — Functions & Advanced Signatures (`functions`)

All exercises in this group have the ID `04xx`.

### Exercise 0401: Function Signatures
* **Topics**: Positional-only/keyword-only arguments, default arguments, return annotations.
* **Scenario**: Math utility function registry.
* **Practice**: Writing robust signatures that restrict parameter calling conventions.

### Exercise 0402: Callables & Overloads
* **Topics**: `Callable[[int], str]`, `@overload` decorator.
* **Scenario**: Event handler registry and polymorphic utility functions.
* **Practice**: Typing functions that accept other functions, and specifying multiple call signatures.

### Exercise 0403: Generators & Asynchrony
* **Topics**: `Generator[yield_type, send_type, return_type]`, `AsyncGenerator`, `Iterable`, `Sequence`.
* **Scenario**: Large dataset streaming processor.
* **Practice**: Annotating stream generators and accepting general container protocols instead of concrete lists.

### Exercise 0404: Decorators & ParamSpec
* **Topics**: `ParamSpec`, `TypeVarTuple`, decorator preservation.
* **Scenario**: Timing or logging decorator.
* **Practice**: Writing decorators that pass through input function arguments and return types without losing static validation.

---

## Group 05 — Generics & Variance (`generics`)

All exercises in this group have the ID `05xx`.

### Exercise 0501: Generic Functions
* **Topics**: `TypeVar("T")`, modern PEP 695 type parameters (e.g. `def func[T](...)`).
* **Scenario**: Generic list utility helpers.
* **Practice**: Writing utility functions that preserve the elements' static types.

### Exercise 0502: Generic Classes
* **Topics**: `Generic[T]`, custom generic containers.
* **Scenario**: Generic cache manager or Repository model.
* **Practice**: Building type-safe generic classes that wrap other objects.

### Exercise 0503: Variance (Covariance & Contravariance)
* **Topics**: `covariant`, `contravariant`, read-only vs. read-write generic collections.
* **Scenario**: Shape drawer accepting collections of base/derived shapes.
* **Practice**: Correctly setting generic boundaries to prevent strict Pyright collection type mismatches.

---

## Group 06 — Structured Data (`structures`)

All exercises in this group have the ID `06xx`.

### Exercise 0601: Enums & Literals
* **Topics**: `enum.Enum`, `Literal["pending", "shipped"]`.
* **Scenario**: E-commerce order status workflow.
* **Practice**: Constraining string values to exact literal options.

### Exercise 0602: TypedDict & Dataclasses
* **Topics**: `typing.TypedDict`, `@dataclass`.
* **Scenario**: Structuring a strict database representation layer.
* **Practice**: Typing dictionary shapes and classes with default fields under strict Pyright configurations.

### Exercise 0603: Type Aliases
* **Topics**: Modern `type` statement, complex nested type aliases.
* **Scenario**: User profile API response structure.
* **Practice**: Declaring clean alias identifiers to simplify nested collection annotations.

---

## Group 07 — Protocols & Structural Typing (`protocols`)

All exercises in this group have the ID `07xx`.

### Exercise 0701: Simple Protocols
* **Topics**: `typing.Protocol`, interface segregation.
* **Scenario**: Mocking external storage (e.g. S3 vs Local) for unit tests without inheritance.
* **Practice**: Writing runtime-free structural contracts to type-check duck-typed components.

### Exercise 0702: Generic Protocols
* **Topics**: `Generic[T]`, `typing.Protocol`.
* **Scenario**: Generic CRUD repository interface.
* **Practice**: Building reusable interfaces that declare generic return and argument parameters.

---

## Group 08 — Dynamic Boundaries & Any (`boundaries`)

All exercises in this group have the ID `08xx`.

### Exercise 0801: Eradicating Any Contagion
* **Topics**: `json.loads()`, `typing.cast`, `Any` containment.
* **Scenario**: Parsing raw external JSON API payloads into TypedDicts.
* **Practice**: Restricting `Any` propagation by explicitly casting or validating dynamic boundaries.

### Exercise 0802: Unknown and Never
* **Topics**: `object`, `Never`, `NoReturn`, exhaustive pattern matching.
* **Scenario**: Exhaustive message queue receiver.
* **Practice**: Utilizing `Never` to ensure type completeness in custom routing logic.

---

## Group 09 — Framework & Library Integration (`integration`)

All exercises in this group have the ID `09xx`.

### Exercise 0901: Pydantic Validation
* **Topics**: `pydantic.BaseModel`, `Field`, nested model definitions.
* **Scenario**: User registration schema validator.
* **Practice**: Constructing models that perform runtime validation matching static type definitions.

### Exercise 0902: FastAPI & Dependency Injection
* **Topics**: `typing.Annotated`, `fastapi.Depends`, path/query parameter typing.
* **Scenario**: REST API backend routes with injected database session.
* **Practice**: Enforcing validation at the HTTP entry and exit points in a type-safe manner.

### Exercise 0903: Ecosystem Boundaries
* **Topics**: `pathlib.Path`, `requests`, `SQLAlchemy` queries.
* **Scenario**: File uploader script talking to a database.
* **Practice**: Addressing common type checker issues when working with third-party libraries and built-in filesystem wrappers.

---

## Group 10 — Capstone Project (`capstone`)

All exercises in this group have the ID `10xx`.

### Exercise 1001: Restore Annotations
* **Scenario**: A complete, broken, and untyped FastAPI service.
* **Practice**: Adding basic type annotations to clear initial Pyright warnings.

### Exercise 1002: Contain the Boundaries
* **Scenario**: Continuing the FastAPI service.
* **Practice**: Restoring types to dynamic boundary logic (`json.loads`, payload requests) and replacing broad `Any` annotations.

### Exercise 1003: Implement Generic Repositories
* **Scenario**: Continuing the FastAPI service.
* **Practice**: Converting database interfaces into generic repository structures that satisfy static type enforcement.

### Exercise 1004: Exhaustive Logic & Strict Pass
* **Scenario**: Continuing the FastAPI service.
* **Practice**: Implementing custom type guards and narrowing patterns to achieve a 100% clean check under strict Pyright mode.
