from re import compile
from decimal import Decimal
from dataclasses import dataclass

from exchanger.exceptions import ExchangeRateException, ExchangeRateTypeMismatch
from exchanger.infrastructure.dto.currency_dto import CurrencyDto


@dataclass
class CreateExchangeRateDto:
    base_currency_dto: CurrencyDto
    target_currency_dto: CurrencyDto
    rate: Decimal

    def __post_init__(self) -> None:
        decimal_pattern = compile(r'^\d+(\.\d+)?$')
        if not isinstance(self.base_currency_dto, CurrencyDto):
            raise ExchangeRateTypeMismatch(
                'Base_currency_dto must be `CurrencyDto` type')

        if not isinstance(self.target_currency_dto, CurrencyDto):
            raise ExchangeRateTypeMismatch(
                'Target_currency_dto must be `CurrencyDto` type')

        if not isinstance(self.rate, (Decimal, str)):
            raise ExchangeRateTypeMismatch(
                f'Rate must be `Decimal` type. Rate type - {type(self.rate)}')

        if not decimal_pattern.match(str(self.rate)):
            raise ExchangeRateException('Rate must be a valid Decimal number')

        self.rate = Decimal(str(self.rate))


@dataclass
class ExchangeRateDto:
    id: int
    base_currency_dto: CurrencyDto
    target_currency_dto: CurrencyDto
    rate: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.id, int):
            raise ExchangeRateTypeMismatch(
                f'Id must be `int` type. Id type - {type(self.id)}')

        if not isinstance(self.base_currency_dto, CurrencyDto):
            raise ExchangeRateTypeMismatch(
                'Base_currency_dto must be `CurrencyDto` type')

        if not isinstance(self.target_currency_dto, CurrencyDto):
            raise ExchangeRateTypeMismatch(
                'Target_currency_dto must be `CurrencyDto` type')

        if not isinstance(self.rate, Decimal):
            raise ExchangeRateTypeMismatch(
                f'Rate must be `Decimal` type. Rate type - {type(self.rate)}')


@dataclass
class ExchangePairDto:
    base_code: str
    target_code: str

    def __post_init__(self) -> None:
        if not isinstance(self.base_code, str):
            raise ExchangeRateTypeMismatch(
                f'Base_code must be `str` type. Id type - {type(self.base_code)}')

        if not isinstance(self.target_code, str):
            raise ExchangeRateTypeMismatch(
                f'Target_code must be `str` type. Id type - {type(self.target_code)}')

        self.base_code = self.base_code.strip()
        self.target_code = self.target_code.strip()
