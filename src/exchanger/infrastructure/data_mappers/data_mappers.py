from abc import abstractmethod
from typing import Protocol, Sequence

from exchanger.core.vo.currency_code import Code
from exchanger.core.models.currency import Currency
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.core.models.exchange_rate import ExchangeRate


class CurrencyDataMapper(Protocol):
    @abstractmethod
    def insert(self, currency: Currency) -> int: ...

    @abstractmethod
    def get_by_code(self, code: Code) -> Currency | None: ...

    @abstractmethod
    def get_all(self) -> Sequence[Currency]: ...


class ExchangeRateDataMapper(Protocol):
    @abstractmethod
    def insert(self, exchange_rate: ExchangeRate) -> int: ...

    @abstractmethod
    def get_by_pair(
        self,
        exchange_pair: ExchangePair
    ) -> ExchangeRate | None: ...

    @abstractmethod
    def get_all(self) -> Sequence[ExchangeRate]: ...
