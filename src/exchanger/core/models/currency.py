from dataclasses import dataclass, field
from re import fullmatch

from exchanger.core.vo.currency_code import Code
from exchanger.exceptions import CurrencyValue


@dataclass(frozen=True)
class Currency:
    code: Code
    name: str
    sign: str
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        if not (3 <= len(self.name) <= 30):
            raise CurrencyValue(
                'Name length must be between 3 and 30 characters')

        if fullmatch(r'[A-Za-z()’ ]+', self.name) is None:
            raise CurrencyValue(
                "Name must contains only letters, spaces, parentheses () and apostrophe ’")

        if not (1 <= len(self.sign) <= 3):
            raise CurrencyValue('Sign length must be between 1 and 3 characters')
