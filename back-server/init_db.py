import sqlite3

from app.settings import BASE_DIR

DSN = BASE_DIR / "db.sqlite3"


def create_db():
    sqlite_db = DSN
    if sqlite_db.exists():
        return

    with sqlite3.connect(str(sqlite_db)) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE messages (
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE,
            value REAL)
        """
        )
        conn.commit()
