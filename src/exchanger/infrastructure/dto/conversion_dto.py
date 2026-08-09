from dataclasses import dataclass
from decimal import Decimal
from re import compile

from exchanger.exceptions import ConversionException
from exchanger.infrastructure.dto.currency_dto import CurrencyDto
from exchanger.infrastructure.dto.exchange_rate_dto import ExchangePairDto


@dataclass
class RequestConversionDto:
    exchange_pair: ExchangePairDto
    amount: Decimal

    def __post_init__(self) -> None:
        decimal_pattern = compile(r'^\d+(\.\d+)?$')
        if not isinstance(self.amount, (Decimal, str)):
            raise ConversionException('Amount must be `Decimal` type')

        if not decimal_pattern.match(str(self.amount)):
            raise ConversionException('Amount must be a valid Decimal number')

        self.amount = Decimal(self.amount)


@dataclass
class ResponseConversionDto:
    base: CurrencyDto
    target: CurrencyDto
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
