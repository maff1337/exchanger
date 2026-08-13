from dataclasses import dataclass
from re import fullmatch

from exchanger.exceptions import CurrencyCodeValue


@dataclass(frozen=True)
class Code:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) != 3:
            raise CurrencyCodeValue(
                f'Code length must be 3 characters. Code - {self.value}, length - {len(self.value)}')

        if not fullmatch(r'[A-Za-z]+', self.value):
            raise CurrencyCodeValue(
                f'Code must contain only latin characters. Code - {self.value}')

        object.__setattr__(self, 'value', self.value.upper())
