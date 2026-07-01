from exchanger.core.vo.currency_code import Code
from exchanger.core.models.currency import Currency
from exchanger.infrastructure.dto.currency_dto import CreateCurrencyDto, CurrencyCodeDto, CurrencyDto


class CurrencyDtoMapper:
    def dto_to_domain(self, currency_dto: CurrencyDto) -> Currency:
        return Currency(
            code=Code(currency_dto.code),
            name=currency_dto.name,
            sign=currency_dto.sign,
            id=currency_dto.id
        )

    def create_dto_to_domain(self, create_currency_dto: CreateCurrencyDto) -> Currency:
        return Currency(
            code=Code(create_currency_dto.code),
            name=create_currency_dto.name,
            sign=create_currency_dto.sign
        )

    def code_dto_to_domain(self, code_dto: CurrencyCodeDto) -> Code:
        return Code(value=code_dto.value)

    def domain_to_dto(self, currency: Currency) -> CurrencyDto:
        if currency.id is None:
            raise ValueError('Id can not be None')

        return CurrencyDto(
            id=currency.id,
            code=currency.code.value,
            name=currency.name,
            sign=currency.sign
        )
