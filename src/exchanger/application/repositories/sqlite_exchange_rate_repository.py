from collections.abc import Sequence
from sqlite3 import IntegrityError

from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.exceptions import (
    ExchangeRateAlreadyExists,
    ExchangeRateException,
    ExchangeRateNotFound,
)
from exchanger.infrastructure.data_mappers.data_mappers import ExchangeRateDataMapper


class SqliteExchangeRateRepository(ExchangeRateRepository):
    def __init__(self, db_exchange_rate_mapper: ExchangeRateDataMapper) -> None:
        self._db_exchange_rate_mapper = db_exchange_rate_mapper

    def create(self, exchange_rate: ExchangeRate) -> int:
        try:
            id = self._db_exchange_rate_mapper.insert(exchange_rate)

            return id
        except IntegrityError:
            raise ExchangeRateAlreadyExists(
                f'Exchange rate {exchange_rate.base.code.value}-{exchange_rate.target.code.value} already exists')

    def find_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate:
        try:
            exchange_rate = self._db_exchange_rate_mapper.get_by_pair(
                exchange_pair)

            return exchange_rate
        except IntegrityError:
            raise ExchangeRateNotFound(
                f'Exchange rate {exchange_pair.base_code.value}-{exchange_pair.target_code.value} not found')

    def find_all(self) -> Sequence[ExchangeRate]:
        try:
            exchange_rates = self._db_exchange_rate_mapper.get_all()

            return exchange_rates
        except IntegrityError as e:
            raise ExchangeRateException(e)
