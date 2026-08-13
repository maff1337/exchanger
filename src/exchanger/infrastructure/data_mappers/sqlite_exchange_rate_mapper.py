from collections.abc import Sequence
from decimal import Decimal
from sqlite3 import Connection, IntegrityError

from exchanger.core.models.currency import Currency
from exchanger.core.models.exchange_rate import ExchangeRate
from exchanger.core.vo.currency_code import Code
from exchanger.core.vo.exchange_pair import ExchangePair, UpdateExchangeRate
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

            query = 'INSERT INTO  exchange_rate (base_currency_id, target_currency_id, rate) VALUES (?, ?, ?) RETURNING id'

            row = cursor.execute(query, (exchange_rate.base.id,
                                         exchange_rate.target.id, str(exchange_rate.rate))).fetchone()

            return row['id']

    def get_by_pair(self, exchange_pair: ExchangePair) -> ExchangeRate:
        with sqlite_cursor(self._conn) as cursor:

            query = '''SELECT er.id as id,
                                c1.code as base_code,
                                c1.full_name as base_name,
                                c1.sign as base_sign,
                                c1.id as base_id,
                                
                                c2.code AS target_code,
                                c2.full_name AS target_name,
                                c2.sign AS target_sign,
                                c2.id AS target_id,
                                er.rate as rate
            FROM exchange_rate AS er
            INNER JOIN currency AS c1 ON c1.id = er.base_currency_id
            INNER JOIN currency AS c2 ON c2.id = er.target_currency_id
            WHERE c1.code = ?
            AND c2.code = ?
            '''

            row = cursor.execute(
                query,
                (exchange_pair.base_code.value, exchange_pair.target_code.value)
            ).fetchone()

            if row:
                return self._row_to_domain(row)
            else:
                raise IntegrityError('Exchange rate not found')

    def get_all(self) -> Sequence[ExchangeRate]:
        with sqlite_cursor(self._conn) as cursor:

            query = '''SELECT er.id as id,
                                c1.code as base_code,
                                c1.full_name as base_name,
                                c1.sign as base_sign,
                                c1.id as base_id,
                                
                                c2.code AS target_code,
                                c2.full_name AS target_name,
                                c2.sign AS target_sign,
                                c2.id AS target_id,
                                er.rate as rate
            FROM exchange_rate AS er
            INNER JOIN currency AS c1 ON c1.id = er.base_currency_id
            INNER JOIN currency AS c2 ON c2.id = er.target_currency_id
            '''

            rows = cursor.execute(query).fetchall()

            return [self._row_to_domain(row) for row in rows]

    def update(self, exchange_rate: UpdateExchangeRate) -> None:
        with sqlite_cursor(self._conn) as cursor:

            update_query = '''UPDATE exchange_rate AS er
                    SET rate = ?
                    WHERE base_currency_id = (SELECT id FROM currency WHERE code = ?)
                    AND target_currency_id = (SELECT id FROM currency WHERE code = ?)
                '''

            cursor.execute(update_query, (str(exchange_rate.rate), exchange_rate.base_code.value,
                                          exchange_rate.target_code.value))

            if cursor.rowcount != 1:
                raise IntegrityError('Not Found')
