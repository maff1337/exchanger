from dataclasses import asdict

from exchanger.application.services.conversion_service import ConversionService
from exchanger.exceptions import (
    ConversionException,
    ExchangeRateException,
    ExchangeRateNotFound,
    NegativeAmount,
)
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto.conversion_dto import RequestConversionDto
from exchanger.infrastructure.dto.exchange_rate_dto import ExchangePairDto
from exchanger.infrastructure.dto_mappers.conversion_mapper import ConversionDtoMapper
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import (
    ExchangeRateDtoMapper,
)


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
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Path parameters are missing'}
                )

            if not isinstance(request.path_params, dict):
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'JSON structure expected'}
                )

            from_curr = request.path_params.get('from')
            to_curr = request.path_params.get('to')
            amount = request.path_params.get('amount')

            if not from_curr:
                raise ConversionException('Query param is missing: from')

            if not to_curr:
                raise ConversionException('Query param is missing: to')

            if not amount:
                raise ConversionException('Query param is missing: amount')

            request_conversion_dto = RequestConversionDto(
                exchange_pair=ExchangePairDto(
                    base_code=from_curr,
                    target_code=to_curr
                ),
                amount=amount
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
        except ExchangeRateNotFound as e:
            return HttpResponse(
                status_code=404,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except (NegativeAmount, ExchangeRateException, ConversionException) as e:
            return HttpResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
