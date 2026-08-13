from sqlite3 import Connection, Row

from exchanger.infrastructure.database.initial_data import (
    INIT_CURRENCY,
    INIT_EXCHANGE_RATE,
)
from exchanger.infrastructure.database.schema import (
    CREATE_CURRENCY_TABLE,
    CREATE_EXCHANGE_RATE_TABLE,
)
from exchanger.infrastructure.database.shared import sqlite_cursor


def init_db(conn: Connection) -> None:
    with sqlite_cursor(conn) as curs:
        conn.row_factory = Row
        curs.execute('PRAGMA foreign_key = ON')

        curs.execute(CREATE_CURRENCY_TABLE)
        curs.execute(CREATE_EXCHANGE_RATE_TABLE)

        curr_insest = '''INSERT OR IGNORE INTO currency (code, full_name, sign) VALUES (?, ?, ?)'''
        er_insert = '''INSERT OR IGNORE INTO exchange_rate (
                            base_currency_id,
                            target_currency_id,
                            rate
                        )
                        SELECT
                            base.id,
                            target.id,
                            ?
                        FROM currency AS base
                        JOIN currency AS target
                        WHERE base.code = ?
                        AND target.code = ?'''

        curs.executemany(curr_insest, INIT_CURRENCY)

        for base, target, rate in INIT_EXCHANGE_RATE:
            curs.execute(er_insert, (rate, base, target))
