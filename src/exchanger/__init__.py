import sqlite3
import tomllib

from exchanger.application.repositories.sqlite_currency_repository import (
    SqliteCurrencyRepository,
)
from exchanger.application.repositories.sqlite_exchange_rate_repository import (
    SqliteExchangeRateRepository,
)
from exchanger.application.services.conversion_service import ConversionService
from exchanger.application.services.currency_service import CurrencyService
from exchanger.application.services.exchange_rate_service import ExchangeRateService
from exchanger.infrastructure.controllers.conversion_controller import (
    HttpConversionController,
)
from exchanger.infrastructure.controllers.currency_controller import (
    HttpCurrencyController,
)
from exchanger.infrastructure.controllers.exchange_rate_controller import (
    HttpExchangeRateController,
)
from exchanger.infrastructure.data_mappers.sqlite_currency_mapper import (
    SqliteCurrencyDataMapper,
)
from exchanger.infrastructure.data_mappers.sqlite_exchange_rate_mapper import (
    SqliteExchangeRateDataMapper,
)
from exchanger.infrastructure.database.initialization import init_db
from exchanger.infrastructure.dto_mappers.conversion_mapper import ConversionDtoMapper
from exchanger.infrastructure.dto_mappers.currency_mapper import CurrencyDtoMapper
from exchanger.infrastructure.dto_mappers.exchange_rate_mapper import (
    ExchangeRateDtoMapper,
)
from exchanger.infrastructure.http.handler import create_handler
from exchanger.infrastructure.http.routing.router import Router
from exchanger.infrastructure.http.server import run_server


def main() -> None:
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    db_path = config['database']['path']

    with sqlite3.connect(db_path) as conn:
        init_db(conn)

        curr_data_mapper = SqliteCurrencyDataMapper(conn)
        er_data_mapper = SqliteExchangeRateDataMapper(conn)

        curr_repo = SqliteCurrencyRepository(curr_data_mapper)
        er_repo = SqliteExchangeRateRepository(er_data_mapper)

        curr_dto_mapper = CurrencyDtoMapper()
        er_dto_mapper = ExchangeRateDtoMapper(curr_dto_mapper)
        conv_dto_mapper = ConversionDtoMapper(curr_dto_mapper, er_dto_mapper)

        curr_service = CurrencyService(curr_repo)
        er_service = ExchangeRateService(er_repo)
        conv_service = ConversionService(er_repo)

        curr_controller = HttpCurrencyController(curr_dto_mapper, curr_service)
        er_controller = HttpExchangeRateController(er_dto_mapper, er_service)
        conv_controller = HttpConversionController(
            conv_dto_mapper, conv_service, er_dto_mapper)

        router = Router()

        router.add_route(
            method='get',
            path='/currencies',
            handler=curr_controller.get_all_currencies
        )

        router.add_route(
            method='get',
            path='/currencies/{code}',
            handler=curr_controller.get_currency_by_code
        )

        router.add_route(
            method='post',
            path='/currencies',
            handler=curr_controller.create_currency
        )

        router.add_route(
            method='patch',
            path='/exchange-rates/{pair}',
            handler=er_controller.update_exchange_rate
        )

        router.add_route(
            method='get',
            path='/exchange-rates',
            handler=er_controller.get_all_rates
        )

        router.add_route(
            method='get',
            path='/exchange-rates/{pair}',
            handler=er_controller.get_exchange_rate_by_pair
        )

        router.add_route(
            method='post',
            path='/exchange-rates',
            handler=er_controller.create_exchange_rate
        )

        router.add_route(
            method='get',
            path='/exchange',
            handler=conv_controller.convert
        )

        handler = create_handler(router)

        host = config["server"]["host"] or config["server"]["default_host"]
        port = config["server"]["port"] or config["server"]["default_port"]

        run_server((host, port), handler)
