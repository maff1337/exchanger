from re import fullmatch
from dataclasses import dataclass, field

from exchanger.core.vo.currency_code import Code


@dataclass(frozen=True)
class Currency:
    code: Code
    name: str
    sign: str
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError('Name must be `str` type')

        if not isinstance(self.sign, str):
            raise TypeError('Sign must be `str` type')

        if not isinstance(self.code, Code):
            raise TypeError('Code must be `Code` type')

        if not (3 <= len(self.name) <= 30):
            raise ValueError('Name length must be between 3 and 30 characters')

        if fullmatch(r'[A-Za-z()’ ]+', self.name) is None:
            raise ValueError(
                "May contain only letters, spaces, parentheses () and apostrophe ’")

        if len(self.sign) != 1:
            raise ValueError('Sign length must be 1 character')
