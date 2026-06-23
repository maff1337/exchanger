from sqlite3 import IntegrityError
from typing import Sequence

from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.exceptions import ExchangeRateException
from exchanger.infrastructure.data_mappers.data_mappers import ExchangeRateDataMapper


class SqliteExchangeRateRepository(ExchangeRateRepository):
    def __init__(self, db_exchange_rate_mapper: ExchangeRateDataMapper) -> None:
        self._db_exchange_rate_mapper = db_exchange_rate_mapper

    def create(self, exchange_rate: ExchangeRate) -> int:
        try:
            id = self._db_exchange_rate_mapper.insert(exchange_rate)

            return id
        except IntegrityError as e:
            raise ExchangeRateException(e)

    def find_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate | None:
        try:
            exchange_rate = self._db_exchange_rate_mapper.get_by_pair(
                exchange_pair)

            return exchange_rate
        except IntegrityError as e:
            raise ExchangeRateException(e)

    def find_all(self) -> Sequence[ExchangeRate]:
        try:
            exchange_rates = self._db_exchange_rate_mapper.get_all()

            return exchange_rates
        except IntegrityError as e:
            raise ExchangeRateException(e)
