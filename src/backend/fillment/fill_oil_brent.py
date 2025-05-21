import csv
import lib

with open("src/backend/fillment/data/oil_brent.csv", "r") as f:
    data = [*csv.reader(f)]

for row in data[1:]:
    open_price = float(row[0])
    close_price = float(row[1])
    price = float(row[0]) + float(row[1])
    
    # sometimes either open_price or close_price may be 0 which isnt correct
    # so it'll take only non-zero value
    # otherwise - an average
    if open_price != 0 or close_price != 0:
        price /= 2

    tmp = row[5].split("/")
    day = tmp[1]
    month = tmp[0]
    year = tmp[2]
    timestamp = f"20{year}-{month}-{day} 10:00:00"

    lib.exec_query(f"insert into brent_crude_oil values ('{timestamp}', {price}, 'USD');")

