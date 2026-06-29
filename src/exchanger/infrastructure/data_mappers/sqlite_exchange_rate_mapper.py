from decimal import Decimal
from sqlite3 import Connection
from typing import Sequence

from exchanger.core.models.currency import Currency
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair
from exchanger.infrastructure.data_mappers.data_mappers import ExchangeRateDataMapper
from exchanger.infrastructure.database.shared import sqlite_cursor


class SqliteExchangeRateDataMapper(ExchangeRateDataMapper):
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def _row_to_domain(self, row) -> ExchangeRate:
        base_currency = Currency(
            code=Code(row['base_code']),
            name=row['base_name'],
            sign=row['base_sign'],
            id=row['base_id']
        )
        target_currency = Currency(
            code=Code(row['target_code']),
            name=row['target_name'],
            sign=row['target_sign'],
            id=row['target_id']
        )

        return ExchangeRate(
            base=base_currency,
            target=target_currency,
            rate=Decimal(row['rate']),
            id=row['id']
        )

    def insert(self, exchange_rate: ExchangeRate) -> int:
        with sqlite_cursor(self._conn) as cursor:

            query = 'INSERT INTO  exchange_rate (base, target, rate) VALUES (?, ?, ?) RETURNING id'

            row = cursor.execute(query, (exchange_rate.base.id,
                                         exchange_rate.target.id, str(exchange_rate.rate))).fetchone()

            return row['id']

    def get_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate | None:
        with sqlite_cursor(self._conn) as cursor:

            query = '''SELECT er.id as id,
                                c1.code as base_code,
                                c1.name as base_name,
                                c1.sign as base_sign,
                                c1.id as base_id,
                                
                                c2.code AS target_code,
                                c2.name AS target_name,
                                c2.sign AS target_sign,
                                c2.id AS target_id,
                                er.rate as rate
            FROM exchange_rate AS er
            INNER JOIN currency AS c1 ON c1.id = er.base
            INNER JOIN currency AS c2 ON c2.id = er.target
            WHERE c1.code = ?
            AND c2.code = ?
            '''

            row = cursor.execute(
                query,
                (exchange_pair.base_code.value, exchange_pair.target_code.value)
            ).fetchone()

            return self._row_to_domain(row) if row else row

    def get_all(self) -> Sequence[ExchangeRate]:
        with sqlite_cursor(self._conn) as cursor:

            query = '''SELECT er.id as id,
                                c1.code as base_code,
                                c1.name as base_name,
                                c1.sign as base_sign,
                                c1.id as base_id,
                                
                                c2.code AS target_code,
                                c2.name AS target_name,
                                c2.sign AS target_sign,
                                c2.id AS target_id,
                                er.rate as rate
            FROM exchange_rate AS er
            INNER JOIN currency AS c1 ON c1.id = er.base
            INNER JOIN currency AS c2 ON c2.id = er.target
            '''

            rows = cursor.execute(query).fetchall()

            return [self._row_to_domain(row) for row in rows]
