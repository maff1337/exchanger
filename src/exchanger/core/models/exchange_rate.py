from dataclasses import dataclass, field
from decimal import Decimal

from exchanger.core.models.currency import Currency
from exchanger.exceptions import CurrencyEquality


@dataclass(frozen=True)
class ExchangeRate:
    base: Currency
    target: Currency
    rate: Decimal
    id: int | None = field(default=None)

    def __post_init__(self) -> None:
        if self.base == self.target:
            raise CurrencyEquality(
                'Base and Target currencies cannot be equals')

        object.__setattr__(self, "rate", max(self.rate, Decimal("0.000001")))
