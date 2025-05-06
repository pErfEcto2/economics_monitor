import lib


for table in lib.sources:
    lib.exec_query(f"create table if not exists {table} (timestamp datetime default current_timestamp primary key, value bigint, units text)")

for table in lib.sources:
    cnt = lib.exec_query(f"select count(*) from {table}")
    
    if cnt and cnt[0][0] > 0:
        continue
    
    raise Exception(f"WARNING, potential missing data in table: {table}")


