from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate


class ExchangeRateRepository(Protocol):
    @abstractmethod
    def create(self, exchange_rate: ExchangeRate) -> ExchangeRate: ...

    @abstractmethod
    def find_by_pair(
        self,
        exchange_pair: ExchangePair
    ) -> ExchangeRate: ...

    @abstractmethod
    def find_all(self) -> Sequence[ExchangeRate]: ...

    @abstractmethod
    def update_by_pair(self, update: UpdateExchangeRate) -> None: ...
    