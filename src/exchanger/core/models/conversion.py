from dataclasses import dataclass
from decimal import Decimal

from exchanger.core.models.currency import Currency
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.exceptions import NegativeAmount


@dataclass(frozen=True)
class RequestConversion:
    exchange_pair: ExchangePair
    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount < Decimal(0):
            raise NegativeAmount(
                f'Amount cannot be negative. Amount - {self.amount}')


@dataclass(frozen=True)
class ResponseConversion:
    base: Currency
    target: Currency
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal
