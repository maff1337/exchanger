from typing import Any


def is_number(value: Any) -> bool:
    try:
        value = float(value)
        return True
    except ValueError:
        return False
