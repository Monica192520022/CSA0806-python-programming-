import csv
import io
import sqlite3
import statistics
import time
import cProfile
import pstats
import random
import pandas as pd

def generate_dataset(num_stations, days=365):
    random.seed(101)
    rows = []
    for s in range(1, num_stations + 1):
        st_name = f"Station_{s:03d}"
        for d in range(1, days + 1):
            day_str = f"2026-{(d-1)//31 + 1:02d}-{(d-1)%31 + 1:02d}"
            for h in range(24):
                rows.append((st_name, day_str, round(random.uniform(15.0, 180.0), 2)))
    return rows

# Method 1A: Plain Python loops + dict of lists + statistics.mean()
def method_python_loops(rows):
    groups = {}
    for st, day, pm in rows:
        groups.setdefault((st, day), []).append(pm)
    return {k: round(statistics.mean(v), 4) for k, v in groups.items()}

# Method 1B: Alternative Concept - One-pass running sum & count in dict
def method_python_onepass(rows):
    acc = {}
    for st, day, pm in rows:
        if (st, day) not in acc:
            acc[(st, day)] = [0.0, 0]
        acc[(st, day)][0] += pm
        acc[(st, day)][1] += 1
    return {k: round(v[0] / v[1], 4) for k, v in acc.items()}

# Method 2: Pandas groupby
def method_pandas(df):
    res = df.groupby(["station", "day"], sort=False)["pm25"].mean().round(4)
    return res.to_dict()

# Method 3: SQLite GROUP BY
def method_sqlite(con):
    cur = con.execute("SELECT station, day, ROUND(AVG(pm25), 4) FROM aq GROUP BY station, day")
    return {(r[0], r[1]): r[2] for r in cur.fetchall()}

if __name__ == "__main__":
    # B3.1 Verify correctness on small data
    small_rows = generate_dataset(2, days=3)
    df_small = pd.DataFrame(small_rows, columns=["station", "day", "pm25"])
    con_small = sqlite3.connect(":memory:")
    con_small.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    con_small.executemany("INSERT INTO aq VALUES (?, ?, ?)", small_rows)

    res_py = method_python_loops(small_rows)
    res_1p = method_python_onepass(small_rows)
    res_pd = method_pandas(df_small)
    res_sq = method_sqlite(con_small)
    con_small.close()

    for k in res_py:
        assert abs(res_py[k] - res_1p[k]) < 1e-3
        assert abs(res_py[k] - res_pd[k]) < 1e-3
        assert abs(res_py[k] - res_sq[k]) < 1e-3

    print("--- B3.1 Correctness Verified ---")
    print("All 4 methods (Python Loops, One-Pass Dict, Pandas, SQLite) match within 1e-4 on small dataset.")
    sample_k = sorted(res_py.keys())[0]
    print(f"Sample Key {sample_k} -> PyLoops: {res_py[sample_k]}, OnePass: {res_1p[sample_k]}, Pandas: {res_pd[sample_k]}, SQLite: {res_sq[sample_k]}")

    # B3.2 Benchmark across 1, 12, and 120 stations over 365 days (8,760 rows/station)
    print("\n--- B3.2 Scaling Benchmark (1, 12, 120 Stations x 8,760 hrs) ---")
    for n_st in [1, 12, 120]:
        rows = generate_dataset(n_st, days=365)
        df = pd.DataFrame(rows, columns=["station", "day", "pm25"])
        con = sqlite3.connect(":memory:")
        con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
        con.executemany("INSERT INTO aq VALUES (?, ?, ?)", rows)

        t0 = time.perf_counter()
        method_python_loops(rows)
        t_py = time.perf_counter() - t0

        t0 = time.perf_counter()
        method_python_onepass(rows)
        t_1p = time.perf_counter() - t0

        t0 = time.perf_counter()
        method_pandas(df)
        t_pd = time.perf_counter() - t0

        t0 = time.perf_counter()
        method_sqlite(con)
        t_sq = time.perf_counter() - t0
        con.close()

        print(f"Stations={n_st:3d} (n={len(rows):7d}) | PyLoops: {t_py*1000:7.2f} ms | PyOnePass: {t_1p*1000:7.2f} ms | Pandas: {t_pd*1000:6.2f} ms | SQLite: {t_sq*1000:6.2f} ms")

    # B3.3 Profile plain-Python version with cProfile on 12 stations (~105,120 rows)
    print("\n--- B3.3 cProfile Output (Plain Python Loops, 12 Stations) ---")
    rows_12 = generate_dataset(12, days=365)
    profiler = cProfile.Profile()
    profiler.enable()
    method_python_loops(rows_12)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("tottime")
    stats.print_stats(8)
