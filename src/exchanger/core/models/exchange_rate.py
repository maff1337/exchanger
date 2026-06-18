from decimal import Decimal
from dataclasses import dataclass, field

from exchanger.core.models.currency import Currency


@dataclass(frozen=True)
class ExchangeRate:
    base: Currency
    target: Currency
    rate: Decimal
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        if not (isinstance(self.base, Currency) and isinstance(self.target, Currency)):
            raise TypeError('Base and Target must be `Currency` type')

        if not isinstance(self.rate, Decimal):
            raise TypeError('Rate must be `Decimal` type')

        if self.base == self.target:
            raise ValueError('Base and Target currencies cannot be equals')
