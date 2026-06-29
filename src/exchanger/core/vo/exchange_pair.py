from dataclasses import dataclass

from exchanger.core.vo.currency_code import Code


@dataclass(frozen=True)
class ExchangePair:
    base_code: Code
    target_code: Code

    def __post_init__(self) -> None:
        if self.base_code == self.target_code:
            raise ValueError('base_code and target_code cannot be equal')
