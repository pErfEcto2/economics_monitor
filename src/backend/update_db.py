import time
import lib
from concurrent.futures import ThreadPoolExecutor


functions = [("brent_crude_oil", lib.get_brent_crude_oil)]
n = len(functions)

assert n == len(lib.sources)

while True:
    time.sleep(5) # change to 5 minutes

    futures = [None] * n

    with ThreadPoolExecutor() as executor:
        for i, f in enumerate(functions):
            futures[i] = executor.submit(f[1])

        for i, f in enumerate(futures):
            res = f.result()
            lib.exec_query(f"insert into {functions[i][0]} values {res}")

