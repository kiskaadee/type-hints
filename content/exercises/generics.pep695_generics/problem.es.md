# Ejercicio 0501: Genéricos Modernos (PEP 695)

Python 3.12 introdujo **PEP 695** (Sintaxis de Parámetros de Tipo), modernizando la forma en que se definen genéricos en Python.

Históricamente, declarar una función o clase genérica requería crear manualmente instancias de `TypeVar` del módulo `typing`:

```python
# Sintaxis anterior (pre-3.12)
from typing import TypeVar, Sequence

T = TypeVar("T")

def first(items: Sequence[T]) -> T:
    return items[0]
```

Con PEP 695, los parámetros de tipo se declaran de forma nativa entre corchetes justo después del nombre de la función o clase:

```python
# Sintaxis moderna PEP 695 (Python 3.12+)
from collections.abc import Sequence

def first[T](items: Sequence[T]) -> T:
    return items[0]
```

---

## Restricciones vs. Límites de Tipo

PEP 695 proporciona sintaxis limpia para limitar o restringir parámetros de tipo:

1. **Límite de Tipo (`[T: BaseClass]`)**:
   Restringe `T` a `BaseClass` o cualquier subclase de `BaseClass`.
2. **Tupla de Restricción (`[T: (TypeA, TypeB)]`)**:
   Restringe `T` estrictamente a uno de los tipos especificados, conservando el tipo concreto entre llamadas:

```python
def stringify[T: (str, int)](value: T) -> str:
    return f"Value: {value}"
```

---

## Clases Genéricas

Las clases declaran parámetros de tipo directamente en la definición de la clase, sin necesidad de heredar de `typing.Generic`:

```python
class Container[T]:
    def __init__(self, item: T) -> None:
        self.item: T = item

    def get(self) -> T:
        return self.item
```

---

## Tu Tarea

Abre el archivo del ejercicio e implementa las anotaciones de tipo utilizando la sintaxis de PEP 695:

1. **`first_or_default`**:
   - Declara el parámetro de tipo `[T]`.
   - Acepta `items: Sequence[T]` y valor por defecto `default: T`.
   - Tipo de retorno `T`.

2. **`format_id`**:
   - Declara el parámetro de tipo con restricción `[T: (str, int)]`.
   - Acepta `val: T`.
   - Tipo de retorno `str`.

3. **`Box`**:
   - Declara la clase genérica `class Box[T]:`.
   - Anota `__init__(self, value: T) -> None`.
   - Anota `get(self) -> T`.
   - Anota `replace(self, new_value: T) -> T`.
