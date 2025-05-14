import csv
import lib

with open("src/backend/fillment/data/oil_brent.csv", "r") as f:
    data = [*csv.reader(f)]

for row in data[1:]:
    price = (float(row[0]) + float(row[1])) / 2
    units = "USD"
    tmp = row[5].split("/")
    day = tmp[1]
    month = tmp[0]
    year = tmp[2]
    timestamp = f"20{year}-{month}-{day} 10:00:00"

    lib.exec_query(f"insert into brent_crude_oil values ('{timestamp}', {price}, 'USD');")

