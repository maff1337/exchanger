from dataclasses import asdict

from exchanger.infrastructure.controllers.types import HttpRequest, HttpResponse
from exchanger.infrastructure.dto_mappers.currency_mapper import CurrencyDtoMapper
from exchanger.application.services.services_protocols import CurrencyServiceProtocol
from exchanger.infrastructure.dto.currency_dto import CreateCurrencyDto, CurrencyCodeDto
from exchanger.exceptions import CurrencyAlreadyExists, CurrencyCodeValue, CurrencyException, CurrencyNotFound, CurrencyValue


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
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Body is missing'}
                )

            body = request.body

            if not isinstance(body, dict):
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'JSON structure expected'}
                )

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

        except CurrencyAlreadyExists as e:
            response = HttpResponse(
                status_code=409,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
            return response
        except (CurrencyException, CurrencyCodeValue, CurrencyValue) as e:
            return HttpResponse(
                400,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except Exception as e:
            response = HttpResponse(
                status_code=500,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
            return response

    def get_currency_by_code(self, request: HttpRequest) -> HttpResponse:
        try:
            if not request.query:
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Query params are missing'}
                )

            code = request.query.get('code')

            if not code:
                return HttpResponse(
                    400,
                    headers={'Content-Type': 'application/json'},
                    body={'message': 'Query param is missing: code'}
                )

            code_dto = CurrencyCodeDto(code)

            currency_dto = self._currency_service.find_by_code(
                code=self._currency_dto_mapper.code_dto_to_domain(code_dto)
            )

            body = asdict(currency_dto)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except CurrencyNotFound as e:
            return HttpResponse(
                404,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except (CurrencyException, CurrencyCodeValue, CurrencyValue) as e:
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

    def get_all_currencies(self, request: HttpRequest) -> HttpResponse:
        try:
            currencies = self._currency_service.find_all()

            body = list(currencies)

            response = HttpResponse(
                200,
                {'Content-Type': 'application/json'},
                body
            )
            return response
        except (CurrencyException, CurrencyCodeValue, CurrencyValue) as e:
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
