from collections.abc import Sequence

from exchanger.application.services.services_protocols import (
    ExchangeRateServiceProtocol,
)
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate


class ExchangeRateService(ExchangeRateServiceProtocol):
    def __init__(self, exchange_rate_repo: ExchangeRateRepository) -> None:
        self._exchange_rate_repo = exchange_rate_repo

    def create(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        er = self._exchange_rate_repo.create(exchange_rate)
        return er

    def find_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate:
        exchange_rate = self._exchange_rate_repo.find_by_pair(exchange_pair)
        return exchange_rate

    def find_all(self) -> Sequence[ExchangeRate]:
        return self._exchange_rate_repo.find_all()

    def update_by_pair(self, update: UpdateExchangeRate) -> None:
        self._exchange_rate_repo.update_by_pair(update)
