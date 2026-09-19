from collections.abc import Sequence
from decimal import Decimal

from exchanger.application.services.services_protocols import (
    ExchangeRateServiceProtocol,
)
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.repositories.currency_repository import CurrencyRepository
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate


class ExchangeRateService(ExchangeRateServiceProtocol):
    def __init__(self, exchange_rate_repo: ExchangeRateRepository, currency_repo: CurrencyRepository) -> None:
        self._exchange_rate_repo = exchange_rate_repo
        self._curr_repo = currency_repo

    def create(self, exchange_pair: ExchangePair, rate: Decimal) -> ExchangeRate:
        base_currency = self._curr_repo.find_by_code(exchange_pair.base_code)
        target_currency = self._curr_repo.find_by_code(
            exchange_pair.target_code)

        er = ExchangeRate(base_currency, target_currency, rate)

        er = self._exchange_rate_repo.create(er)
        return er

    def find_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate:
        exchange_rate = self._exchange_rate_repo.find_by_pair(exchange_pair)
        return exchange_rate

    def find_all(self) -> Sequence[ExchangeRate]:
        return self._exchange_rate_repo.find_all()

    def update_by_pair(self, update: UpdateExchangeRate) -> None:
        self._exchange_rate_repo.update_by_pair(update)
