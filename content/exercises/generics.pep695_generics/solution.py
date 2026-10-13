"""
Solution for Exercise 0501: Modern Generics (PEP 695).
"""

from collections.abc import Sequence


def first_or_default[T](items: Sequence[T], default: T) -> T:
    if items:
        return items[0]
    return default


def format_id[T: (str, int)](val: T) -> str:
    return f"ID-{val}"


class Box[T]:
    def __init__(self, value: T) -> None:
        self._value: T = value

    def get(self) -> T:
        return self._value

    def replace(self, new_value: T) -> T:
        old: T = self._value
        self._value = new_value
        return old


if __name__ == "__main__":
    nums = [1, 2, 3]
    first_num: int = first_or_default(nums, 0)
    print(f"First num: {first_num}")

    formatted: str = format_id(42)
    print(f"Formatted: {formatted}")

    box: Box[str] = Box("initial")
    old_val: str = box.replace("updated")
    print(f"Replaced: {old_val} -> {box.get()}")
