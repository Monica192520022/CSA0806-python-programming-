# b4_index.py - effect of an index on the slowest query (120 stations, 1,051,200 rows)
import csv
import os
import sqlite3
import time
import pandas as pd

if os.path.exists("big.db"):
    os.remove("big.db")
con = sqlite3.connect("big.db")
con.execute("CREATE TABLE r (station TEXT, day TEXT, hour INTEGER, pm25 REAL)")
with open("year_120.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    con.executemany("INSERT INTO r VALUES (?, ?, ?, ?)", ((a, b, int(c), float(d)) for a, b, c, d in reader))
con.commit()

QUERY = "SELECT AVG(pm25) FROM r WHERE station = ? AND day BETWEEN '2026-10-01' AND '2026-10-31'"


def time_query(repeat=20):
    start = time.perf_counter()
    for i in range(repeat):
        result = con.execute(QUERY, ("S057",)).fetchone()[0]
    return (time.perf_counter() - start) / repeat, result


t_before, answer = time_query()
print("Plan before index:", con.execute("EXPLAIN QUERY PLAN " + QUERY, ("S057",)).fetchall()[0][-1])
start = time.perf_counter()
con.execute("CREATE INDEX idx_station_day ON r (station, day)")
build = time.perf_counter() - start
t_after, answer2 = time_query()
print("Plan after index :", con.execute("EXPLAIN QUERY PLAN " + QUERY, ("S057",)).fetchall()[0][-1])
print("Answer (same both times):", round(answer, 2), round(answer2, 2))
print("Query time WITHOUT index:", round(t_before * 1000, 2), "ms")
print("Query time WITH index   :", round(t_after * 1000, 2), "ms")
print("Speed-up: about", round(t_before / t_after), "times | index build time:", round(build, 2), "s")
con.close()
print("Database size (MB):", round(os.path.getsize("big.db") / 1e6, 1))

# alternative: pandas reads the whole CSV for every question
start = time.perf_counter()
df = pd.read_csv("year_120.csv")
t_load = time.perf_counter() - start
start = time.perf_counter()
m = df[(df.station == "S057") & (df.day >= "2026-10-01") & (df.day <= "2026-10-31")].pm25.mean()
t_filter = time.perf_counter() - start
print("pandas: load CSV", round(t_load, 2), "s, filter", round(t_filter * 1000, 1), "ms, answer", round(m, 2))
print("DataFrame memory (MB):", round(df.memory_usage(deep=True).sum() / 1e6, 1))
