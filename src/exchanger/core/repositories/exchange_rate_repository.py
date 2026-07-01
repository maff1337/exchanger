from abc import abstractmethod
from typing import Protocol, Sequence

from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.core.models.exchange_rate import ExchangeRate


class ExchangeRateRepository(Protocol):
    @abstractmethod
    def create(self, exchange_rate: ExchangeRate) -> int: ...

    @abstractmethod
    def find_by_pair(
        self, exchange_pair: ExchangePair
    ) -> ExchangeRate | None: ...

    @abstractmethod
    def find_all(self) -> Sequence[ExchangeRate]: ...
