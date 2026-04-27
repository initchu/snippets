import sqlite3
from contextlib import contextmanager


@contextmanager
def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# 2026-04-27 06:13:15
