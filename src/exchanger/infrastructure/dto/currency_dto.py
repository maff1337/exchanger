from dataclasses import dataclass

from exchanger.exceptions import CurrencyTypeMismatch


@dataclass
class CurrencyDto:
    id: int
    code: str
    name: str
    sign: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int):
            raise CurrencyTypeMismatch(
                f'Id must be `int` type. Id type - {type(self.id)}')

        if not isinstance(self.code, str):
            raise CurrencyTypeMismatch(
                f'Code must be `str` type. Code type - {type(self.code)}')

        if not isinstance(self.name, str):
            raise CurrencyTypeMismatch(
                f'Name must be `str` type. Name type - {type(self.name)}')

        if not isinstance(self.code, str):
            raise CurrencyTypeMismatch(
                f'Sign must be `str` type. Sign type - {type(self.sign)}')

        object.__setattr__(self, 'code', self.code.strip())
        object.__setattr__(self, 'name', self.name.strip())
        object.__setattr__(self, 'sign', self.sign.strip())


@dataclass
class CreateCurrencyDto:
    code: str
    name: str
    sign: str

    def __post_init__(self) -> None:
        if not isinstance(self.code, str):
            raise CurrencyTypeMismatch(
                f'Code must be `str` type. Code type - {type(self.code)}')

        if not isinstance(self.name, str):
            raise CurrencyTypeMismatch(
                f'Name must be `str` type. Code type - {type(self.name)}')

        if not isinstance(self.code, str):
            raise CurrencyTypeMismatch(
                f'Sign must be `str` type. Code type - {type(self.sign)}')

        object.__setattr__(self, 'code', self.code.strip())
        object.__setattr__(self, 'name', self.name.strip())
        object.__setattr__(self, 'sign', self.sign.strip())


@dataclass
class CurrencyCodeDto:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise CurrencyTypeMismatch(
                f'Code must be `str` type. Code type - {type(self.value)}')

        object.__setattr__(self, 'code', self.value.strip())
