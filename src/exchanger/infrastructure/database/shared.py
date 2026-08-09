from contextlib import contextmanager
from sqlite3 import Connection


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
