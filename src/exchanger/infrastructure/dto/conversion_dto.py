from decimal import Decimal
from dataclasses import dataclass

from exchanger.exceptions import ConversionException
from exchanger.infrastructure.dto.currency_dto import CurrencyDto
from exchanger.infrastructure.dto.exchange_rate_dto import ExchangePairDto


@dataclass
class RequestConversionDto:
    exchange_pair: ExchangePairDto
    amount: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.amount, (Decimal, str)):
            raise ConversionException('Amount must be `Decimal` type')

        if not str.isnumeric(str(self.amount)):
            raise ConversionException('Amount must be a valid number')

        self.amount = Decimal(self.amount)


@dataclass
class ResponseConversionDto:
    base: CurrencyDto
    target: CurrencyDto
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
