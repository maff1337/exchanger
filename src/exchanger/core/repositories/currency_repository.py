from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from exchanger.core.models.currency import Currency
from exchanger.core.vo.currency_code import Code


class CurrencyRepository(Protocol):
    @abstractmethod
    def create(self, currency: Currency) -> Currency: ...

    @abstractmethod
    def find_by_code(self, code: Code) -> Currency: ...

    @abstractmethod
    def find_all(self) -> Sequence[Currency]: ...
