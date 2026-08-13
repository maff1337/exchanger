from exchanger.application.services.services_protocols import CurrencyServiceProtocol
from exchanger.exceptions import (
    CurrencyAlreadyExists,
    CurrencyCodeValue,
    CurrencyException,
    CurrencyNotFound,
    CurrencyValue,
)
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
                raise CurrencyException('Body is missing')

            body = request.body

            if not isinstance(body, dict):
                raise CurrencyException('JSON structure expected')

            code = body.get('code')
            name = body.get('name')
            sign = body.get('sign')

            if not code:
                raise CurrencyException('Body param is missing: code')

            if not name:
                raise CurrencyException('Body param is missing: name')

            if not sign:
                raise CurrencyException('Body param is missing: sign')

            currency_dto = CreateCurrencyDto(
                code=code,
                name=name,
                sign=sign
            )
            currency_dto = self._currency_dto_mapper.domain_to_dto(
                self._currency_service.create(
                    currency=self._currency_dto_mapper.create_dto_to_domain(
                        currency_dto)
                )
            )

            body = currency_dto.as_dict()

            response = HttpResponse(
                status_code=201, 
                headers={'Content-Type': 'application/json'}, 
                body=body
            )
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
                status_code=400,
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
            if not request.path_params:
                raise CurrencyException('Path params are missing')
                

            code = request.path_params.get('code')

            if not code:
                raise CurrencyException('Path param is  missing: code')

            code_dto = CurrencyCodeDto(code)

            currency_dto = self._currency_dto_mapper.domain_to_dto(
                    self._currency_service.find_by_code(
                    code=self._currency_dto_mapper.code_dto_to_domain(code_dto)
                )
            )

            body = currency_dto.as_dict()

            response = HttpResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=body
            )
            return response
        except CurrencyNotFound as e:
            return HttpResponse(
                status_code=404,
                headers={'Content-Type': 'application/json'},
                body={'message': str(e)}
            )
        except (CurrencyException, CurrencyCodeValue, CurrencyValue) as e:
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

    def get_all_currencies(self, request: HttpRequest) -> HttpResponse:
        try:
            currencies = self._currency_service.find_all()
            currencies = [self._currency_dto_mapper.domain_to_dto(currency) for currency in currencies]

            body = [currency.as_dict() for currency in currencies]

            response = HttpResponse(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                body=body
            )
            return response
        except (CurrencyException, CurrencyCodeValue, CurrencyValue) as e:
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
