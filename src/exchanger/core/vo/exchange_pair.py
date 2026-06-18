from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangePair:
    base_id: int
    target_id: int

    def __post_init__(self) -> None:
        if not (isinstance(self.base_id, int) and isinstance(self.target_id, int)):
            raise TypeError('base_id and target_id must be `int` type')

        if self.base_id <= 0 or self.target_id <= 0:
            raise ValueError('base_id and target_id must be positive')

        if self.base_id == self.target_id:
            raise ValueError('base_id and target_id cannot be equal')
