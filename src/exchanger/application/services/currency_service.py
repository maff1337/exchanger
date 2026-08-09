from collections.abc import Sequence

from exchanger.application.services.services_protocols import CurrencyServiceProtocol
from exchanger.core.models.currency import Currency
from exchanger.core.repositories.currency_repository import CurrencyRepository
from exchanger.core.vo.currency_code import Code


class CurrencyService(CurrencyServiceProtocol):
    def __init__(self, currency_repo: CurrencyRepository) -> None:
        self._currency_repo = currency_repo

    def create(self, currency: Currency) -> int:
        id = self._currency_repo.create(currency)
        return id

    def find_by_code(self, code: Code) -> Currency:
        currency = self._currency_repo.find_by_code(code)

        return currency

    def find_all(self) -> Sequence[Currency]:
        return self._currency_repo.find_all()
