from abc import abstractmethod
from typing import Protocol, Sequence

from exchanger.core.vo.currency_code import Code
from exchanger.core.models.currency import Currency
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.models.conversion import RequestConversion, ResponseConversion


class CurrencyServiceProtocol(Protocol):
    @abstractmethod
    def create(self, currency: Currency) -> int: ...

    @abstractmethod
    def find_by_code(self, code: Code) -> Currency | None: ...

    @abstractmethod
    def find_all(self) -> Sequence[Currency]: ...


class ExchangeRateServiceProtocol(Protocol):
    @abstractmethod
    def create(self, exchange_rate: ExchangeRate) -> int: ...

    @abstractmethod
    def find_by_pair(
        self,
        exchange_pair: ExchangePair
    ) -> ExchangeRate | None: ...

    @abstractmethod
    def find_all(self) -> Sequence[ExchangeRate]: ...


class ConversionServiceProtocol(Protocol):
    @abstractmethod
    def convert(
        self,
        request_conversion: RequestConversion
    ) -> ResponseConversion: ...
