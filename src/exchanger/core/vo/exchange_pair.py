from dataclasses import dataclass

from exchanger.core.vo.currency_code import Code
from exchanger.exceptions import CurrencyCodeEquality


@dataclass(frozen=True)
class ExchangePair:
    base_code: Code
    target_code: Code

    def __post_init__(self) -> None:
        if self.base_code == self.target_code:
            raise CurrencyCodeEquality('Base code and Target code cannot be equal')
