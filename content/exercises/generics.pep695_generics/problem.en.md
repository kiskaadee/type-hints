# Exercise 0501: Modern Generics (PEP 695)

Python 3.12 introduced **PEP 695** (Type Parameter Syntax), revolutionizing how generics are defined in Python.

Historically, declaring a generic function or class required manually creating `TypeVar` objects from the `typing` module:

```python
# Legacy syntax (pre-3.12)
from typing import TypeVar, Sequence

T = TypeVar("T")

def first(items: Sequence[T]) -> T:
    return items[0]
```

With PEP 695, type parameters are declared natively inside square brackets directly after the function or class name:

```python
# Modern PEP 695 syntax (Python 3.12+)
from collections.abc import Sequence

def first[T](items: Sequence[T]) -> T:
    return items[0]
```

---

## Type Constraints vs. Bounds

PEP 695 provides clean syntax for constraining or bounding type parameters:

1. **Type Bound (`[T: BaseClass]`)**:
   Restricts `T` to `BaseClass` or any subclass of `BaseClass`.
2. **Type Constraints (`[T: (TypeA, TypeB)]`)**:
   Restricts `T` to strictly one of the specified types, preserving the concrete type across calls:

```python
def stringify[T: (str, int)](value: T) -> str:
    return f"Value: {value}"
```

---

## Generic Classes

Classes declare type parameters directly on the class statement without inheriting from `typing.Generic`:

```python
class Container[T]:
    def __init__(self, item: T) -> None:
        self.item: T = item

    def get(self) -> T:
        return self.item
```

---

## Your Task

Open the exercise file and implement the type annotations using PEP 695 syntax:

1. **`first_or_default`**:
   - Declare type parameter `[T]`.
   - Accept `items: Sequence[T]` and fallback `default: T`.
   - Return type `T`.

2. **`format_id`**:
   - Declare constrained type parameter `[T: (str, int)]`.
   - Accept `val: T`.
   - Return type `str`.

3. **`Box`**:
   - Declare generic class `class Box[T]:`.
   - Annotate `__init__(self, value: T) -> None`.
   - Annotate `get(self) -> T`.
   - Annotate `replace(self, new_value: T) -> T`.
