from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from exchanger.core.models.currency import Currency
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate


class CurrencyDataMapper(Protocol):
    @abstractmethod
    def insert(self, currency: Currency) -> int: ...

    @abstractmethod
    def get_by_code(self, code: Code) -> Currency: ...

    @abstractmethod
    def get_all(self) -> Sequence[Currency]: ...


class ExchangeRateDataMapper(Protocol):
    @abstractmethod
    def insert(self, exchange_rate: ExchangeRate) -> int: ...

    @abstractmethod
    def get_by_pair(
        self,
        exchange_pair: ExchangePair
    ) -> ExchangeRate: ...

    @abstractmethod
    def get_all(self) -> Sequence[ExchangeRate]: ...

    @abstractmethod
    def update(self, exchange_rate: UpdateExchangeRate) -> None: ...
    