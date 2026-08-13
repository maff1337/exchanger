from dataclasses import dataclass
from decimal import Decimal

from exchanger.core.vo.currency_code import Code
from exchanger.exceptions import CurrencyCodeEquality, NegativeAmount


@dataclass(frozen=True)
class ExchangePair:
    base_code: Code
    target_code: Code

    def __post_init__(self) -> None:
        if self.base_code == self.target_code:
            raise CurrencyCodeEquality('Base code and Target code cannot be equal')


@dataclass(frozen=True)
class UpdateExchangeRate:
    base_code: Code
    target_code: Code
    rate: Decimal
    
    def __post_init__(self) -> None:
        object.__setattr__(self, 'rate', Decimal(self.rate))
        
        if self.rate < Decimal(0):
            raise NegativeAmount(f'Rate must be non-negative value. Rate - {self.rate}')

        if self.base_code == self.target_code:
            raise CurrencyCodeEquality('Base code and Target code cannot be equal')