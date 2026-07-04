from sqlite3 import Connection
from contextlib import contextmanager


@contextmanager
def sqlite_cursor(conn: Connection):
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
