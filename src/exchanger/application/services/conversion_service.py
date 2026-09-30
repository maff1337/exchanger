from decimal import Decimal
from enum import Enum

from exchanger.application.services.services_protocols import ConversionServiceProtocol
from exchanger.core.models.conversion import RequestConversion, ResponseConversion
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.repositories.exchange_rate_repository import ExchangeRateRepository
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.exceptions import ExchangeRateNotFound


class RateDirection(Enum):
    BASE_TO_TARGET = "base_to_target"
    TARGET_TO_BASE = "target_to_base"


class ConversionService(ConversionServiceProtocol):
    def __init__(self, exchange_rate_repo: ExchangeRateRepository) -> None:
        self._exchange_rate_repo = exchange_rate_repo

    def _get_rate(self, first: Code, second: Code) -> tuple[ExchangeRate, RateDirection]:
        try:
            rate = self._exchange_rate_repo.find_by_pair(
                ExchangePair(first, second))
            return rate, RateDirection.BASE_TO_TARGET
        except ExchangeRateNotFound:
            rate = self._exchange_rate_repo.find_by_pair(
                ExchangePair(second, first))
            return rate, RateDirection.TARGET_TO_BASE

    def convert(self, request_conversion: RequestConversion) -> ResponseConversion:
        base_code = request_conversion.exchange_pair.base_code
        target_code = request_conversion.exchange_pair.target_code
        usd_code = Code('usd')

        try:
            exchange_rate, direction = self._get_rate(base_code, target_code)

            if direction == RateDirection.TARGET_TO_BASE:
                base_currency = exchange_rate.target
                target_currency = exchange_rate.base

                rate = Decimal(1) / exchange_rate.rate
            else:
                base_currency = exchange_rate.base
                target_currency = exchange_rate.target

                rate = exchange_rate.rate

        except ExchangeRateNotFound:
            if base_code == usd_code or target_code == usd_code:
                raise ExchangeRateNotFound(
                    f'Exchange rate for {base_code.value}-{target_code.value} not found')

            try:
                base_er, base_direction = self._get_rate(base_code, usd_code)
                target_er, target_direction = self._get_rate(
                    target_code, usd_code)

                if (base_direction == RateDirection.BASE_TO_TARGET
                        and target_direction == RateDirection.BASE_TO_TARGET):
                    base_currency = base_er.base
                    target_currency = target_er.base

                    rate = base_er.rate / target_er.rate

                elif (base_direction == RateDirection.TARGET_TO_BASE
                      and target_direction == RateDirection.TARGET_TO_BASE):
                    base_currency = base_er.target
                    target_currency = target_er.target

                    rate = target_er.rate / base_er.rate

                else:
                    base_currency = base_er.base if base_direction == RateDirection.BASE_TO_TARGET else base_er.target
                    target_currency = target_er.base if target_direction == RateDirection.BASE_TO_TARGET else target_er.target

                    rate = (
                        base_er.rate * target_er.rate
                        if base_direction == RateDirection.BASE_TO_TARGET
                        else Decimal(1) / (base_er.rate * target_er.rate)
                    )

            except ExchangeRateNotFound:
                raise ExchangeRateNotFound(
                    f'Exchange rate for {base_code.value}-{target_code.value} not found')

        rate = rate.quantize(Decimal('0.000001'))
        converted_amount = request_conversion.amount * rate

        return ResponseConversion(
            base=base_currency,
            target=target_currency,
            rate=rate,
            amount=request_conversion.amount,
            converted_amount=converted_amount.quantize(Decimal('0.000001'))
        )
