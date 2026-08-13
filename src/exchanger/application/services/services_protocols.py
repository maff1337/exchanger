from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from exchanger.core.models.conversion import RequestConversion, ResponseConversion
from exchanger.core.models.currency import Currency
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate


class CurrencyServiceProtocol(Protocol):
    @abstractmethod
    def create(self, currency: Currency) -> Currency: ...

    @abstractmethod
    def find_by_code(self, code: Code) -> Currency: ...

    @abstractmethod
    def find_all(self) -> Sequence[Currency]: ...


class ExchangeRateServiceProtocol(Protocol):
    @abstractmethod
    def create(self, exchange_rate: ExchangeRate) -> int: ...

    @abstractmethod
    def find_by_pair(
        self,
        exchange_pair: ExchangePair
    ) -> ExchangeRate: ...

    @abstractmethod
    def find_all(self) -> Sequence[ExchangeRate]: ...

    @abstractmethod
    def update_by_pair(self, update: UpdateExchangeRate) -> None: ...


class ConversionServiceProtocol(Protocol):
    @abstractmethod
    def convert(
        self,
        request_conversion: RequestConversion
    ) -> ResponseConversion: ...
