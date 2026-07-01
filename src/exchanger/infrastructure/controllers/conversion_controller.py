from dataclasses import asdict

from exchanger.application.services.conversion_service import ConversionService
from exchanger.core.models.conversion import RequestConversion
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto.conversion_dto import RequestConversionDto
from exchanger.infrastructure.dto.exchange_rate_dto import ExchangePairDto
from exchanger.infrastructure.dto_mappers.conversion_mapper import ConversionDtoMapper
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import ExchangeRateDtoMapper


class HttpConversionController:
    def __init__(
        self,
        conversion_dto_mapper: ConversionDtoMapper,
        conversion_service: ConversionService,
        exchange_rate_dto_mapper: ExchangeRateDtoMapper,

    ) -> None:
        self._conversion_dto_mapepr = conversion_dto_mapper
        self._conversion_service = conversion_service
        self._exchange_rate_dto_mapper = exchange_rate_dto_mapper

    def convert(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.path_params:
                raise AttributeError('Qurry param is missing: path_params')

            if not isinstance(request.path_params, dict):
                raise TypeError('JSON structure expected')

            request_conversion_dto = RequestConversionDto(
                exchange_pair=ExchangePairDto(
                    base_code=request.path_params['from'],
                    target_code=request.path_params['to']
                ),
                amount=request.path_params['amount']
            )

            response_conversion = self._conversion_service.convert(
                request_conversion=self._conversion_dto_mapepr.request_dto_to_domain(
                    request_conversion_dto
                )
            )

            body = asdict(response_conversion)
            response = HttpResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=body
            )
            return response

        except Exception:
            raise
