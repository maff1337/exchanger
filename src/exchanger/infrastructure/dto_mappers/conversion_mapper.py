from exchanger.core.models.conversion import RequestConversion, ResponseConversion
from exchanger.infrastructure.dto.conversion_dto import (
    RequestConversionDto,
    ResponseConversionDto,
)
from exchanger.infrastructure.dto_mappers.currency_mapper import CurrencyDtoMapper
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import (
    ExchangeRateDtoMapper,
)


class ConversionDtoMapper:
    def __init__(
        self,
        currency_dto_mapper: CurrencyDtoMapper,
        exchange_rate_dto_mapper: ExchangeRateDtoMapper
    ) -> None:
        self._currency_mapper = currency_dto_mapper
        self._exchange_rate_mapper = exchange_rate_dto_mapper

    def request_dto_to_domain(self, dto: RequestConversionDto) -> RequestConversion:
        exchange_pair = self._exchange_rate_mapper.pair_dto_to_domain(
            dto.exchange_pair
        )

        return RequestConversion(
            exchange_pair,
            dto.amount
        )

    def domain_to_response_dto(self, domain: ResponseConversion) -> ResponseConversionDto:
        base_currency_dto = self._currency_mapper.domain_to_dto(
            domain.base
        )
        target_currency_dto = self._currency_mapper.domain_to_dto(
            domain.target
        )

        return ResponseConversionDto(
            base=base_currency_dto,
            target=target_currency_dto,
            rate=domain.rate,
            amount=domain.amount,
            converted_amount=domain.converted_amount
        )
