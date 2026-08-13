from decimal import Decimal

from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate
from exchanger.infrastructure.dto.exchange_rate_dto import (
    CreateExchangeRateDto,
    ExchangePairDto,
    ExchangeRateDto,
    UpdateExchangeRateDto,
)
from exchanger.infrastructure.dto_mappers.currency_mapper import CurrencyDtoMapper


class ExchangeRateDtoMapper:
    def __init__(self, currency_dto_mapper: CurrencyDtoMapper) -> None:
        self._currency_mapper = currency_dto_mapper

    def create_dto_to_domain(self, dto: CreateExchangeRateDto) -> ExchangeRate:
        base_currency = self._currency_mapper.dto_to_domain(
            dto.base_currency_dto
        )
        target_currency = self._currency_mapper.dto_to_domain(
            dto.target_currency_dto
        )

        return ExchangeRate(
            base=base_currency,
            target=target_currency,
            rate=dto.rate
        )

    def dto_to_domain(self, dto: ExchangeRateDto) -> ExchangeRate:
        base_currency = self._currency_mapper.dto_to_domain(
            dto.base
        )
        target_currency = self._currency_mapper.dto_to_domain(
            dto.target
        )

        return ExchangeRate(
            base=base_currency,
            target=target_currency,
            rate=Decimal(dto.rate),
            id=dto.id
        )

    def domain_to_dto(self, domain: ExchangeRate) -> ExchangeRateDto:
        base_currency_dto = self._currency_mapper.domain_to_dto(
            domain.base
        )
        target_currency_dto = self._currency_mapper.domain_to_dto(
            domain.target
        )

        if domain.id is None:
            raise ValueError('Id cannot be None')

        return ExchangeRateDto(
            id=domain.id,
            base=base_currency_dto,
            target=target_currency_dto,
            rate=str(domain.rate)
        )

    def pair_dto_to_domain(self, pair_dto: ExchangePairDto) -> ExchangePair:
        return ExchangePair(
            Code(pair_dto.base_code),
            Code(pair_dto.target_code)
        )

    def update_to_domain(self, update: UpdateExchangeRateDto) -> UpdateExchangeRate:
        return UpdateExchangeRate(
            Code(update.base_code),
            Code(update.target_code),
            rate=Decimal(update.rate)
        )
