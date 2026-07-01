from dataclasses import asdict
from decimal import Decimal

from exchanger.application.services.services_protocols import ExchangeRateServiceProtocol
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto.currency_dto import CurrencyDto
from exchanger.infrastructure.dto.exchange_rate_dto import CreateExchangeRateDto, ExchangePairDto
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import ExchangeRateDtoMapper


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
                raise AttributeError('Body is missing')

            body = request.body

            if not isinstance(body, dict):
                raise TypeError('JSON structure expected')

            exchange_rate_dto = CreateExchangeRateDto(
                base_currency_dto=CurrencyDto(
                    id=body['baseCurrency']['id'],
                    code=body['baseCurrency']['code'],
                    name=body['baseCurrency']['fullName'],
                    sign=body['baseCurrency']['sign']
                ),
                target_currency_dto=CurrencyDto(
                    id=body['targetCurrency']['id'],
                    code=body['targetCurrency']['code'],
                    name=body['targetCurrency']['fullName'],
                    sign=body['targetCurrency']['sign']
                ),
                rate=Decimal(body['rate'])
            )

            id = self._er_service.create(
                self._er_dto_mapper.create_dto_to_domain(exchange_rate_dto)
            )

            body = {'id': id}

            response = HttpResponse(
                204, {'Content-Type': 'application/json'}, body)
            return response

        except Exception:
            raise

    def get_exchange_rate_by_pair(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.query:
                raise AttributeError('Query params are missing')

            pair = request.query['pair']
            if not pair:
                raise AttributeError('Query param is missing: pair')

            if not isinstance(pair, str):
                raise TypeError('Pair is not a `str` type')

            if len(pair) != 6:
                raise ValueError(
                    'Pair is not a valid exchange pair')

            exchange_pair_dto = ExchangePairDto(pair[:3], pair[3:])

            exchange_rate_dto = self._er_service.find_by_pair(
                exchange_pair=self._er_dto_mapper.pair_dto_to_domain(
                    exchange_pair_dto
                )
            )

            if exchange_rate_dto is None:
                raise ValueError()

            body = asdict(exchange_rate_dto)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except Exception:
            raise

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
        except Exception:
            raise
