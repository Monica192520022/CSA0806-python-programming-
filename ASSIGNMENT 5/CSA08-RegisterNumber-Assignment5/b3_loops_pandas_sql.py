# b3_loops_pandas_sql.py - daily mean PM2.5 per station in three ways (+ running sum)
import csv
import os
import random
import sqlite3
import statistics
import time

import pandas as pd

random.seed(5)


def make_file(stations, path):
    """One year of hourly readings (8,760 per station): station, day, hour, pm25"""
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["station", "day", "hour", "pm25"])
        for s in range(stations):
            name = "S" + str(s).zfill(3)
            for m, d_count in enumerate(days_in_month, start=1):
                for d in range(1, d_count + 1):
                    day = "2026-%02d-%02d" % (m, d)
                    for h in range(24):
                        w.writerow([name, day, h, round(random.uniform(20, 150), 1)])


def method_loops(path):
    groups = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["station"], row["day"])
            groups.setdefault(key, []).append(float(row["pm25"]))     # stores ALL readings
    return {k: round(statistics.mean(v), 3) for k, v in groups.items()}


def method_running_sum(path):
    total = {}
    count = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            key = (row["station"], row["day"])
            total[key] = total.get(key, 0) + float(row["pm25"])       # keeps only a sum and a count
            count[key] = count.get(key, 0) + 1
    return {k: round(total[k] / count[k], 3) for k in total}


def method_pandas(path):
    df = pd.read_csv(path)
    result = df.groupby(["station", "day"])["pm25"].mean().round(3)
    return {k: v for k, v in result.items()}


def method_sql(path):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE r (station TEXT, day TEXT, hour INTEGER, pm25 REAL)")
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        con.executemany("INSERT INTO r VALUES (?, ?, ?, ?)",
                        ((a, b, int(c), float(d)) for a, b, c, d in reader))
    start = time.perf_counter()
    rows = con.execute("SELECT station, day, ROUND(AVG(pm25), 3) FROM r GROUP BY station, day").fetchall()
    query_time = time.perf_counter() - start
    con.close()
    return {(a, b): c for a, b, c in rows}, query_time


if __name__ == "__main__":
    # B3.1 correctness on small data: 1 station
    make_file(1, "year_1.csv")
    a = method_loops("year_1.csv")
    b = method_pandas("year_1.csv")
    c, _ = method_sql("year_1.csv")
    d = method_running_sum("year_1.csv")
    same = all(abs(a[k] - b[k]) < 0.0011 and abs(a[k] - c[k]) < 0.0011 and abs(a[k] - d[k]) < 0.0011 for k in a)
    print("Groups:", len(a), "| all four methods agree:", same, "| first group:", list(a.items())[0])

    # B3.2 time for 1, 12 and 120 stations
    print("\nstations rows      loops   running  pandas   SQL(load+query)  SQL query only")
    for stations in (1, 12, 120):
        path = "year_" + str(stations) + ".csv"
        if not os.path.exists(path):
            make_file(stations, path)
        rows = stations * 8760
        t = time.perf_counter(); method_loops(path); t1 = time.perf_counter() - t
        t = time.perf_counter(); method_running_sum(path); t2 = time.perf_counter() - t
        t = time.perf_counter(); method_pandas(path); t3 = time.perf_counter() - t
        t = time.perf_counter(); _, q = method_sql(path); t4 = time.perf_counter() - t
        print(str(stations).ljust(8), str(rows).ljust(9), round(t1, 2), "  ", round(t2, 2), "  ", round(t3, 2),
              "  ", round(t4, 2), "           ", round(q, 2))
