from typing import Sequence
from sqlite3 import Connection

from exchanger.core.vo.currency_code import Code
from exchanger.core.models.currency import Currency
from exchanger.infrastructure.database.shared import sqlite_cursor
from exchanger.infrastructure.data_mappers.data_mappers import CurrencyDataMapper


class SqliteCurrencyDataMapper(CurrencyDataMapper):
    def __init__(self, connection: Connection) -> None:
        self._conn = connection

    def _row_to_domain(self, row) -> Currency:
        return Currency(
            code=Code(row['code']),
            name=row['name'],
            sign=row['sign'],
            id=row['id']
        )

    def insert(self, currency: Currency) -> int:
        with sqlite_cursor(self._conn) as cursor:
            query = 'INSERT INTO currency (code, name, sign) VALUES (?, ?, ?) RETURNING id'

            row = cursor.execute(
                query,
                (currency.code.value, currency.name, currency.sign)
            ).fetchone()

            return row['id']

    def get_by_code(self, code: Code) -> Currency | None:
        with sqlite_cursor(self._conn) as cursor:
            query = 'SELECT * FROM currency WHERE code = ?'

            row = cursor.execute(query, (code.value,)).fetchone()

            return self._row_to_domain(row) if row else row

    def get_all(self) -> Sequence[Currency]:
        with sqlite_cursor(self._conn) as cursor:
            query = 'SELECT * FROM currency'

            rows = cursor.execute(query).fetchall()

            return [self._row_to_domain(row) for row in rows]
