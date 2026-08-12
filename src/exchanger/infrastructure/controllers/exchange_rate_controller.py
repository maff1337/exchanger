from dataclasses import asdict

from exchanger.application.services.services_protocols import (
    ExchangeRateServiceProtocol,
)
from exchanger.exceptions import (
    CurrencyCodeEquality,
    CurrencyEquality,
    ExchangeRateAlreadyExists,
    ExchangeRateException,
    ExchangeRateNotFound,
    ExchangeRateTypeMismatch,
    NegativeAmount,
)
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto.currency_dto import CurrencyDto
from exchanger.infrastructure.dto.exchange_rate_dto import (
    CreateExchangeRateDto,
    ExchangePairDto,
)
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import (
    ExchangeRateDtoMapper,
)


class HttpExchangeRateController:
    def __init__(
        self,
        exchange_rate_dto_mapper: ExchangeRateDtoMapper,
        exchange_rate_service: ExchangeRateServiceProtocol
    ) -> None:
        self._er_dto_mapper = exchange_rate_dto_mapper
        self._er_service = exchange_rate_service

    def create_exchange_rate(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.body:
                raise ExchangeRateException('Body is missing')

            body = request.body

            if not isinstance(body, dict):
                raise ExchangeRateException('JSON structure expected')

            base_currency = body.get('baseCurrency')
            target_currency = body.get('targetCurrency')
            rate = body.get('rate')

            if not base_currency:
                raise ExchangeRateException(
                    'Body param is missing: baseCurrency')

            if not target_currency:
                raise ExchangeRateException(
                    'Body param is missing: targetCurrency')

            if not rate:
                raise ExchangeRateException('Body param is missing: rate')

            base_c_id = base_currency.get('id')
            base_c_code = base_currency.get('code')
            base_c_name = base_currency.get('name')
            base_c_sign = base_currency.get('sign')

            target_c_id = target_currency.get('id')
            target_c_code = target_currency.get('code')
            target_c_name = target_currency.get('name')
            target_c_sign = target_currency.get('sign')

            if not base_c_id:
                raise ExchangeRateException(
                    'Body param is missing: baseCurrency: id')

            if not base_c_code:
                raise ExchangeRateException(
                    'Body param is missing: baseCurrency: code')

            if not base_c_name:
                raise ExchangeRateException(
                    'Body param is missing: baseCurrency: name')

            if not base_c_sign:
                raise ExchangeRateException(
                    'Body param is missing: baseCurrency: sign')

            if not target_c_id:
                raise ExchangeRateException(
                    'Body param is missing: targetCurrency: id')

            if not target_c_code:
                raise ExchangeRateException(
                    'Body param is missing: targetCurrency: code')

            if not target_c_name:
                raise ExchangeRateException(
                    'Body param is missing: targetCurrency: name')

            if not target_c_sign:
                raise ExchangeRateException(
                    'Body param is missing: targetCurrency: sign')

            exchange_rate_dto = CreateExchangeRateDto(
                base_currency_dto=CurrencyDto(
                    id=base_c_id,
                    code=base_c_code,
                    name=base_c_name,
                    sign=base_c_sign
                ),
                target_currency_dto=CurrencyDto(
                    id=target_c_id,
                    code=target_c_code,
                    name=target_c_name,
                    sign=target_c_sign
                ),
                rate=rate
            )

            id = self._er_service.create(
                self._er_dto_mapper.create_dto_to_domain(exchange_rate_dto)
            )

            body = {'id': id}

            response = HttpResponse(
                201,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except ExchangeRateAlreadyExists as e:
            return HttpResponse(
                status_code=409,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except (NegativeAmount, ExchangeRateException, CurrencyEquality, CurrencyCodeEquality, ExchangeRateTypeMismatch) as e:
            return HttpResponse(
                400,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )

    def get_exchange_rate_by_pair(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.path_params:
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Path params params are missing'}
                )

            pair = request.path_params.get('pair')
            if not pair:
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Path params param is missing: pair'}
                )

            if len(pair) != 6:
                raise ExchangeRateException(
                    'Pair is not a valid exchange pair')

            exchange_pair_dto = ExchangePairDto(pair[:3], pair[3:])

            exchange_rate_dto = self._er_service.find_by_pair(
                exchange_pair=self._er_dto_mapper.pair_dto_to_domain(
                    exchange_pair_dto
                )
            )

            body = asdict(exchange_rate_dto)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except ExchangeRateNotFound as e:
            return HttpResponse(
                404,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except (NegativeAmount, ExchangeRateException, CurrencyEquality, CurrencyCodeEquality, ExchangeRateTypeMismatch) as e:
            return HttpResponse(
                400,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )

    def get_all_rates(self, _: HttpRequest | None = None) -> HttpResponse:
        try:
            rates = self._er_service.find_all()

            body = list(rates)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except (NegativeAmount, ExchangeRateException, CurrencyEquality, CurrencyCodeEquality, ExchangeRateTypeMismatch) as e:
            return HttpResponse(
                400,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
