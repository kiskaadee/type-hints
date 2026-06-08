# Course Outline

Exercises are designed to challenge the learner to implement type annotations with increasing level of complexity, exercising active research and muscle memory. This isn't focus on teaching any other language features or patterns rather than type annotations in different use cases.

---

# Planned Learning Path

## Module 1 — Primitive Types

### Exercise 0101

Basic variable annotations.

Topics:

* `str`
* `int`
* `float`
* `bool`

Example scenario:

Employee onboarding profile.

Students only fill:

```python
employee_name: ???
employee_id: ???
hourly_rate: ???
is_full_time: ???
```

No collections yet.

---

## Module 2 — Collection Types

### Exercise 0102

Introduce:

```python
list[str]
tuple[float, float]
set[str]
dict[str, str]
```

Use your current employee example.

Topics:

* homogeneous collections
* key/value structures
* immutable vs mutable collections

---

## Module 3 — Optional Values

### Exercise 0103

Introduce:

```python
str | None
Optional[str]
```

Scenario:

Customer support ticket.

Some fields may not exist yet.

```python
assigned_agent: str | None
resolution_notes: str | None
```

Important because FastAPI and Pydantic use this constantly.

---

## Module 4 — Function Annotations

### Exercise 0104

Introduce:

```python
def calculate_total(price: float, tax: float) -> float:
```

Topics:

* parameter types
* return types

This is where type hints become genuinely useful.

---

## Module 5 — Complex Collections

### Exercise 0105

Introduce nesting.

```python
list[dict[str, str]]
dict[str, list[str]]
```

Scenario:

Inventory system.

---

## Module 6 — Type Aliases

### Exercise 0106

Introduce:

```python
type UserId = int

type Email = str
```

or

```python
UserId = int
```

depending on Python version.

Useful for larger codebases.

---

## Module 7 — TypedDict

### Exercise 0107

Introduce:

```python
from typing import TypedDict
```

```python
class User(TypedDict):
    name: str
    age: int
```

This is often the student's first encounter with structured data typing.

---

## Module 8 — Dataclasses

### Exercise 0108

Introduce:

```python
@dataclass
class User:
    ...
```

Topics:

* modeling data
* replacing dictionaries

---

## Module 9 — Enums

### Exercise 0109

Introduce:

```python
from enum import Enum
```

```python
class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
```

Very common in APIs.

---

## Module 10 — Literal Types

### Exercise 0110

Introduce:

```python
Literal["pending", "approved", "rejected"]
```

Students start seeing type systems as constraints, not just documentation.

---

## Module 11 — Union Types

### Exercise 0111

```python
str | int
```

and

```python
Union[str, int]
```

Understanding multiple accepted types.

---

## Module 12 — Generics

### Exercise 0112

Introduce:

```python
list[T]
dict[K, V]
```

and eventually

```python
TypeVar
```

---

## Module 13 — Protocols

### Exercise 0113

Introduce structural typing.

```python
Protocol
```

This is advanced but extremely valuable.

---

## Module 14 — Pydantic Models

### Exercise 0114

First real FastAPI-style model.

```python
class UserCreate(BaseModel):
    ...
```

---

## Module 15 — Nested Pydantic Models

### Exercise 0115

```python
class Address(BaseModel):
    ...

class User(BaseModel):
    address: Address
```

---

## Module 16 — FastAPI Request Models

### Exercise 0116

Typing request bodies.

```python
@app.post("/users")
```

---

## Module 17 — Response Models

### Exercise 0117

```python
response_model=UserResponse
```

---

## Module 18 — Dependency Injection Typing

### Exercise 0118

Introduce:

```python
Annotated
```

```python
db: Annotated[Session, Depends(get_db)]
```

Very FastAPI-specific.

---

## Module 19 — Generic Pydantic Models

### Exercise 0119

```python
ApiResponse[T]
```

Common API pattern.

---

## Module 20 — Real Project Review

Students receive a minimal but realistic FastAPI codebase full of missing annotations and must restore them.

This becomes the capstone.
