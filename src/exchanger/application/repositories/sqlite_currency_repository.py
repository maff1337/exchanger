from sqlite3 import IntegrityError
from typing import Sequence

from exchanger.core.models.currency import Currency
from exchanger.core.repositories.currency_repository import CurrencyRepository
from exchanger.core.vo.currency_code import Code
from exchanger.exceptions import CurrencyException
from exchanger.infrastructure.data_mappers.data_mappers import CurrencyDataMapper


class SqliteCurrencyRepository(CurrencyRepository):
    def __init__(self, db_currency_mapper: CurrencyDataMapper) -> None:
        self._db_currency_mapper = db_currency_mapper

    def create(self, currency: Currency) -> int:
        try:
            id = self._db_currency_mapper.insert(currency)

            return id
        except IntegrityError as e:
            raise CurrencyException(e)

    def find_by_code(self, code: Code) -> Currency | None:
        try:
            currency = self._db_currency_mapper.get_by_code(code)

            return currency
        except IntegrityError as e:
            raise CurrencyException(e)

    def find_all(self) -> Sequence[Currency]:
        try:
            currencies = self._db_currency_mapper.get_all()

            return currencies
        except IntegrityError as e:
            raise CurrencyException(e)
