from dataclasses import asdict

from exchanger.application.services.services_protocols import CurrencyServiceProtocol
from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto.currency_dto import CreateCurrencyDto, CurrencyCodeDto
from exchanger.infrastructure.dto_mappers.currency_mapper import CurrencyDtoMapper


class HttpCurrencyController:
    def __init__(
        self,
        currency_dto_mapper: CurrencyDtoMapper,
        currency_service: CurrencyServiceProtocol
    ) -> None:
        self._currency_dto_mapper = currency_dto_mapper
        self._currency_service = currency_service

    def create_currency(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.body:
                raise AttributeError('Body is missing')

            body = request.body
            if not body:
                raise AttributeError('Body is missing')

            if not isinstance(body, dict):
                raise TypeError('JSON structure expected')

            currency_dto = CreateCurrencyDto(
                code=body['code'],
                name=body['fullName'],
                sign=body['sign']
            )
            id = self._currency_service.create(
                currency=self._currency_dto_mapper.create_dto_to_domain(
                    currency_dto)
            )

            body = {'id': id}

            response = HttpResponse(
                204, {'Content-Type': 'application/json'}, body)
            return response

        except Exception:
            raise

    def get_currency_by_code(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.query:
                raise AttributeError('Query param is missing: code')

            code = request.query.get('code')

            if not code:
                raise AttributeError('Query param is missing: code')
            code_dto = CurrencyCodeDto(code)

            currency_dto = self._currency_service.find_by_code(
                code=self._currency_dto_mapper.code_dto_to_domain(code_dto)
            )

            if currency_dto is None:
                raise ValueError()

            body = asdict(currency_dto)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except Exception:
            raise

    def get_all_currencies(self, request: HttpRequest) -> HttpResponse:
        try:
            currencies = self._currency_service.find_all()

            body = list(currencies)

            response = HttpResponse(
                200, {'Content-Type': 'application/json'}, body)
            return response
        except Exception:
            raise
