import lib


for table in lib.sources:
    lib.exec_query(f"""create table if not exists {table} (timestamp datetime default current_timestamp primary key, value bigint, units text)""")

# initial fill at the first startup

