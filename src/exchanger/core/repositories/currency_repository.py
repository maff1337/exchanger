from abc import abstractmethod
from typing import Protocol, Sequence

from exchanger.core.vo.currency_code import Code
from exchanger.core.models.currency import Currency


class CurrencyRepository(Protocol):
    @abstractmethod
    def create(self, currency: Currency) -> int: ...

    @abstractmethod
    def find_by_code(self, code: Code) -> Currency | None: ...

    @abstractmethod
    def find_all(self) -> Sequence[Currency]: ...
