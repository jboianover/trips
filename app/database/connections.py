from sqlalchemy import create_engine, text
import os
from typing import Any


def __get_conn():

    engine = create_engine(os.environ['DATABASE_URL'])

    return engine.connect()


def _fetch_rows(query: str) -> Any:

    with __get_conn() as conn:
        result = conn.execute(text(query))
    conn.close()
    return result
