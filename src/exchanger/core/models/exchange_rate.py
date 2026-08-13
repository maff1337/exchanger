from dataclasses import dataclass, field
from decimal import Decimal

from exchanger.core.models.currency import Currency
from exchanger.exceptions import CurrencyEquality, NegativeAmount


@dataclass
class ExchangeRate:
    base: Currency
    target: Currency
    rate: Decimal
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        if self.base == self.target:
            raise CurrencyEquality(
                'Base and Target currencies cannot be equals')

        if self.rate < 0:
            raise NegativeAmount('Exchange rate cannot be negative')
