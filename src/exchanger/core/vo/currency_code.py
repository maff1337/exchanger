from re import fullmatch
from dataclasses import dataclass


@dataclass(frozen=True)
class Code:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError(
                f'Code must be string. Code type - {type(self.value)}')

        if len(self.value) != 3:
            raise ValueError(
                f'Code length must be 3 characters. Code - {self.value}, length - {len(self.value)}')

        if not fullmatch(r'[A-Za-z]+', self.value):
            raise ValueError(
                f'Code must contain only latin characters. Code - {self.value}')

        object.__setattr__(self, 'value', self.value.upper())
