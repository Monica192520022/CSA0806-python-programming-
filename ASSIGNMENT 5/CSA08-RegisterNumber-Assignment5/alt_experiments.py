# alt_experiments.py - measurements for the "Alternative Concept" parts
import csv, io, logging, os, random, sqlite3, sys, time, tracemalloc
import pandas as pd

random.seed(2)

# ---- B1: csv loops versus pandas cleaning (1,000 / 100,000 / 1,000,000 rows)
def make_pm_file(n, path):
    with open(path, "w") as f:
        f.write("station,date,pm25\n")
        for i in range(n):
            r = random.random()
            value = "NA" if r < 0.02 else "" if r < 0.04 else "-5" if r < 0.05 else str(round(random.uniform(10, 200), 1))
            f.write("S" + str(i % 12) + ",2026-10-01," + value + "\n")


def loops(path):
    values = []
    with open(path) as f:
        for r in csv.DictReader(f):
            v = r["pm25"].strip()
            if v == "" or v == "NA":
                continue
            v = float(v)
            if v < 0 or v > 999:
                continue
            values.append(v)
    low, high = min(values), max(values)
    return [(v - low) / (high - low) for v in values]


def with_pandas(path):
    df = pd.read_csv(path, na_values=["NA", ""])
    df = df[(df.pm25 >= 0) & (df.pm25 <= 999)].dropna(subset=["pm25"])
    return (df.pm25 - df.pm25.min()) / (df.pm25.max() - df.pm25.min())


print("B1 alternative: rows | loops time, peak MB | pandas time, peak MB")
for n in (1000, 100000, 1000000):
    make_pm_file(n, "pm.csv")
    out = []
    for func in (loops, with_pandas):
        start = time.perf_counter(); func("pm.csv"); t = time.perf_counter() - start
        tracemalloc.start(); func("pm.csv"); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        out.append((round(t, 3), round(peak / 1e6, 1)))
    print("  ", n, out[0], out[1])
os.remove("pm.csv")

# ---- A2: drop versus forward fill (daily means) using the October files
from clean import clean_file, to_number
print("\nA2 alternative: drop missing readings instead of filling (mean PM2.5 of October)")
for name in ["Adyar", "Guindy"]:
    rows, _ = clean_file("data/raw_" + name + ".csv")
    filled = {}
    for r in rows:
        filled.setdefault(r["day"], []).append(r["pm25"])
    dropped = {}
    with open("data/raw_" + name + ".csv") as f:
        seen = set()
        for r in csv.DictReader(f):
            v = to_number(r["pm25"])
            key = (r["date"], r["hour"])
            if v is None or v < 0 or v > 999 or key in seen:
                continue
            seen.add(key)
            dropped.setdefault(r["date"], []).append(v)
    mf = sum(sum(v) for v in filled.values()) / sum(len(v) for v in filled.values())
    md = sum(sum(v) for v in dropped.values()) / sum(len(v) for v in dropped.values())
    biggest = max(abs(sum(filled[d]) / len(filled[d]) - sum(dropped[d]) / len(dropped[d])) for d in filled)
    print("  ", name, "| readings kept: fill", sum(len(v) for v in filled.values()), "drop",
          sum(len(v) for v in dropped.values()), "| month mean fill", round(mf, 2), "drop", round(md, 2),
          "| largest daily difference", round(biggest, 2))
data = [random.random() for _ in range(200000)]
start = time.perf_counter(); sorted(data)[len(data) // 2]; t_median = time.perf_counter() - start
start = time.perf_counter(); last = None; out = []
for v in data:
    last = v if v > 0.01 else last
    out.append(last)
t_ffill = time.perf_counter() - start
start = time.perf_counter(); [v for v in data if v > 0.01]; t_drop = time.perf_counter() - start
print("   time for 200,000 values: drop", round(t_drop * 1000, 1), "ms | forward fill", round(t_ffill * 1000, 1),
      "ms | median by sorting", round(t_median * 1000, 1), "ms")

# ---- A4: print versus logging versus logging switched off (100,000 calls)
print("\nA4 alternative: cost of 100,000 debug messages")
real_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")
start = time.perf_counter()
for i in range(100000):
    print("reading", i, "value", i * 0.5)
t_print = time.perf_counter() - start
sys.stdout = real_stdout
logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG, format="%(levelname)s %(message)s")
start = time.perf_counter()
for i in range(100000):
    logging.debug("reading %s value %s", i, i * 0.5)
t_log_on = time.perf_counter() - start
logging.getLogger().setLevel(logging.WARNING)             # switch off DEBUG messages
start = time.perf_counter()
for i in range(100000):
    logging.debug("reading %s value %s", i, i * 0.5)
t_log_off = time.perf_counter() - start
print("   print:", round(t_print, 3), "s | logging at DEBUG (to file):", round(t_log_on, 3),
      "s | logging at WARNING (switched off):", round(t_log_off, 3), "s")
logging.shutdown(); os.remove("debug.log")

# ---- B2: executemany versus execute in a loop
print("\nB2 alternative: inserting n rows")
rows_all = [("S" + str(i % 12), "2026-10-01", float(i % 200)) for i in range(100000)]
for n in (1000, 10000, 100000):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    start = time.perf_counter()
    con.executemany("INSERT INTO aq VALUES (?, ?, ?)", rows_all[:n])
    con.commit()
    t1 = time.perf_counter() - start
    con.execute("DELETE FROM aq")
    start = time.perf_counter()
    for r in rows_all[:n]:
        con.execute("INSERT INTO aq VALUES (?, ?, ?)", r)
    con.commit()
    t2 = time.perf_counter() - start
    print("  ", n, "executemany:", round(t1, 4), "s | execute in loop:", round(t2, 4), "s")
    con.close()
