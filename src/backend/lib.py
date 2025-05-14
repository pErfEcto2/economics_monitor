import sqlite3
import config
from typing import Any
import requests
from bs4 import BeautifulSoup
from datetime import timezone, datetime


sources = ["brent_crude_oil"]


def exec_query(query: str) -> list[tuple] | list:
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

def get_brent_crude_oil() -> tuple | None:
    try:
        soup = BeautifulSoup(requests.get("https://markets.businessinsider.com/commodities/oil-price").content, "html5lib")
        price = float(soup.find_all("span", attrs={"class": "price-section__current-value"})[0].text)
        t = datetime.now(timezone.utc)

    except Exception:
        return
    
    return (f"{t.year}-{str(t.month).zfill(2)}-{str(t.day).zfill(2)} {str(t.hour).zfill(2)}:{str(t.minute).zfill(2)}:{str(t.second).zfill(2)}", price, "USD")

