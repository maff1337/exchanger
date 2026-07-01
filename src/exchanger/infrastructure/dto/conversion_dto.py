from decimal import Decimal
from dataclasses import dataclass

from exchanger.infrastructure.dto.currency_dto import CurrencyDto
from exchanger.infrastructure.dto.exchange_rate_dto import ExchangePairDto


@dataclass
class RequestConversionDto:
    exchange_pair: ExchangePairDto
    amount: Decimal


@dataclass
class ResponseConversionDto:
    base: CurrencyDto
    target: CurrencyDto
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
