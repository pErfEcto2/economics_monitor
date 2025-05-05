import sqlite3
import config
from typing import Any


sources = ["brent_crude_oil"]


def exec_query(query: str) -> list[tuple] | None:
    with sqlite3.connect(config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        res = cursor.fetchall()
        cursor.close()
    return res

def query_res_to_dict(query_res: list[tuple] | None, keys: list[str]) -> list[dict[str, Any]] | None:
    if query_res is None or len(query_res) == 0:
        return None

    res = []
    n = len(keys)
    for row in query_res:
        if len(row) != n:
            return None

        res.append({k: v for k, v in zip(keys, row)})
    
    return res




