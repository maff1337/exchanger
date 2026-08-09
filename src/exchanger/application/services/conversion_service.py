from decimal import Decimal

from exchanger.application.services.services_protocols import ConversionServiceProtocol
from exchanger.core.models.conversion import RequestConversion, ResponseConversion
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.exceptions import ExchangeRateNotFound


class ConversionService(ConversionServiceProtocol):
    def __init__(self, exchange_rate_repo: ExchangeRateRepository) -> None:
        self._exchange_rate_repo = exchange_rate_repo

    def convert(self, request_conversion: RequestConversion) -> ResponseConversion:
        base_code = request_conversion.exchange_pair.base_code
        target_code = request_conversion.exchange_pair.target_code
        usd_code = Code('usd')

        exchange_rate = self._exchange_rate_repo.find_by_pair(
            request_conversion.exchange_pair
        )

        if exchange_rate is None:
            new_base_code, new_target_code = target_code, base_code

            exchange_rate = self._exchange_rate_repo.find_by_pair(
                ExchangePair(new_base_code, new_target_code)
            )

            if exchange_rate is None:
                if base_code == usd_code or target_code == usd_code:
                    raise ExchangeRateNotFound(
                        f'Exchange rate for {base_code.value}-{target_code.value} not found')

                new_base_pair = ExchangePair(base_code, usd_code)
                new_target_pair = ExchangePair(target_code, usd_code)

                base_usd = self._exchange_rate_repo.find_by_pair(
                    new_base_pair
                )
                target_usd = self._exchange_rate_repo.find_by_pair(
                    new_target_pair
                )

                if base_usd is None or target_usd is None:
                    raise ExchangeRateNotFound(
                        f'Exchange rate for {base_code.value}-{target_code.value} not found')
                else:
                    base_currency = base_usd.base
                    target_currency = target_usd.base

                    rate = base_usd.rate / target_usd.rate
            else:
                base_currency = exchange_rate.target
                target_currency = exchange_rate.base

                rate = Decimal(1) / exchange_rate.rate
        else:
            base_currency = exchange_rate.base
            target_currency = exchange_rate.target

            rate = exchange_rate.rate

        converted_amount = request_conversion.amount * rate

        return ResponseConversion(
            base=base_currency,
            target=target_currency,
            rate=rate,
            amount=request_conversion.amount,
            converted_amount=converted_amount
        )
