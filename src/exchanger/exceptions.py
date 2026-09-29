class UnsupportedMediaType(Exception):
    ...


class CurrencyException(Exception):
    ...


class CurrencyValue(CurrencyException):
    ...


class CurrencyCodeValue(Exception):
    ...


class CurrencyAlreadyExists(CurrencyException):
    ...


class CurrencyNotFound(Exception):
    ...


class ExchangeRateException(Exception):
    ...


class ExchangeRateAlreadyExists(ExchangeRateException):
    ...


class ExchangeRateNotFound(Exception):
    ...


class CurrencyEquality(Exception):
    ...


class CurrencyCodeEquality(Exception):
    ...


class CurrencyTypeMismatch(CurrencyException):
    ...


class ExchangeRateTypeMismatch(ExchangeRateException):
    ...


class NegativeAmount(Exception):
    ...


class ConversionException(Exception):
    ...
