import csv
import os
import sqlite3
import time
import tracemalloc
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_CSV = os.path.join(BASE_DIR, "raw_station_readings.csv")
CLEAN_CSV = os.path.join(BASE_DIR, "cleaned_station_readings.csv")
DB_PATH = os.path.join(BASE_DIR, "air_quality.db")

# 1. Generate realistic raw sample dataset containing all A1.1 issues
def create_sample_raw_csv():
    random.seed(42)
    stations = ["Adyar", "Guindy", "Anna Nagar", "T. Nagar", "Velachery", "Perambur"]
    fahrenheit_stations = {"Anna Nagar", "Perambur"}
    rows = [
        ["station_name", "date", "hour", "pm25", "pm10", "no2", "temperature"],
        # Deliberate data-quality edge cases from A1.1
        [" adyar ", "01-10-2026", "0", "48.2", "85.0", "24.1", "29.5"],
        ["Adyar", "2026/10/01", "0", "48.2", "85.0", "24.1", "29.5"],   # Duplicate row
        ["Adyar", "2026-10-01", "1", "NA", "82.0", "22.0", "29.0"],     # Single missing -> forward fill
        ["Adyar", "2026-10-01", "2", "", "80.0", "21.5", "28.8"],       # Consecutive missing -> drop
        ["Guindy", "2026-10-01", "3", "-14.5", "90.0", "30.0", "28.0"], # Negative impossible value
        ["Guindy", "2026-10-01", "4", "9999.0", "95.0", "31.2", "28.5"],# Hardware spike > 999
        ["Anna Nagar", "2026-10-01", "12", "64.0", "110.0", "35.0", "89.6"], # Fahrenheit (89.6F = 32.0C)
    ]

    start_date = datetime(2026, 10, 1)
    for day_offset in range(30):
        curr_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for st in stations:
            base_pm = {"Adyar": 45, "Guindy": 78, "Anna Nagar": 62, "T. Nagar": 85, "Velachery": 55, "Perambur": 70}[st]
            for hr in range(0, 24, 3):
                if day_offset == 0 and hr < 6:
                    continue
                rush = 20 if hr in (9, 18, 21) else 0
                pm25 = round(max(12.0, random.gauss(base_pm + rush, 10)), 2)
                pm10 = round(pm25 * 1.65, 2)
                no2 = round(max(8.0, random.gauss(28 + rush * 0.5, 6)), 2)
                temp_c = round(27.0 + (5.0 if 12 <= hr <= 15 else 0.0) + random.uniform(-1.5, 1.5), 2)
                temp_val = round(temp_c * 9 / 5 + 32, 2) if st in fahrenheit_stations else temp_c
                rows.append([st, curr_date, str(hr), str(pm25), str(pm10), str(no2), str(temp_val)])

    with open(RAW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def standardise_date(d_str):
    d_str = d_str.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(d_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

def clean_pipeline(input_csv):
    seen_keys = set()
    last_valid_pm25 = {}
    cleaned = []
    fahrenheit_stations = {"Anna Nagar", "Perambur"}

    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            st = " ".join(row["station_name"].strip().split()).title()
            dt = standardise_date(row["date"])
            try:
                hr = int(row["hour"].strip())
            except ValueError:
                continue

            if not st or not dt or not (0 <= hr <= 23):
                continue

            key = (st, dt, hr)
            if key in seen_keys:
                continue

            raw_pm25 = row["pm25"].strip()
            if not raw_pm25 or raw_pm25.upper() in ("NA", "NULL", "NAN"):
                if (st, dt) in last_valid_pm25:
                    pm25 = last_valid_pm25[(st, dt)]
                    # Clear after 1-step forward fill so multi-hour gaps are dropped
                    del last_valid_pm25[(st, dt)]
                else:
                    continue
            else:
                try:
                    pm25 = float(raw_pm25)
                except ValueError:
                    continue
                if not (0.0 <= pm25 <= 999.0):
                    continue
                last_valid_pm25[(st, dt)] = pm25

            try:
                pm10 = float(row["pm10"].strip())
                no2 = float(row["no2"].strip())
                temp = float(row["temperature"].strip())
            except ValueError:
                continue

            if not (0.0 <= pm10 <= 1500.0 and 0.0 <= no2 <= 500.0):
                continue

            if st in fahrenheit_stations or temp > 55.0:
                temp = (temp - 32.0) * (5.0 / 9.0)

            if not (-5.0 <= temp <= 55.0):
                continue

            seen_keys.add(key)
            cleaned.append([st, dt, hr, round(pm25, 2), round(pm10, 2), round(no2, 2), round(temp, 2)])

    # Compute Min-Max and Z-Score normalisation for PM2.5
    pm_vals = [r[3] for r in cleaned]
    lo, hi = min(pm_vals), max(pm_vals)
    mean_pm = sum(pm_vals) / len(pm_vals)
    std_pm = (sum((x - mean_pm) ** 2 for x in pm_vals) / len(pm_vals)) ** 0.5

    for r in cleaned:
        mm = round((r[3] - lo) / (hi - lo), 3) if hi > lo else 0.0
        zs = round((r[3] - mean_pm) / std_pm, 3) if std_pm > 0 else 0.0
        r.extend([mm, zs])

    with open(CLEAN_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station_name", "obs_date", "obs_hour", "pm25", "pm10", "no2", "temp_c", "pm25_minmax", "pm25_zscore"])
        writer.writerows(cleaned)

    return cleaned

def load_to_sqlite(cleaned_rows):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE stations (
            station_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT NOT NULL UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE readings (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER NOT NULL,
            obs_date TEXT NOT NULL,
            obs_hour INTEGER NOT NULL,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            temp_c REAL,
            pm25_minmax REAL,
            pm25_zscore REAL,
            UNIQUE(station_id, obs_date, obs_hour),
            FOREIGN KEY(station_id) REFERENCES stations(station_id)
        )
    """)

    unique_stations = sorted({r[0] for r in cleaned_rows})
    cur.executemany("INSERT INTO stations (station_name) VALUES (?)", [(s,) for s in unique_stations])
    cur.execute("SELECT station_name, station_id FROM stations")
    st_map = dict(cur.fetchall())

    db_rows = [
        (st_map[r[0]], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
        for r in cleaned_rows
    ]
    cur.executemany(
        """INSERT INTO readings
           (station_id, obs_date, obs_hour, pm25, pm10, no2, temp_c, pm25_minmax, pm25_zscore)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        db_rows
    )
    con.commit()

    print("\n--- B1.3 SQLite Query Results ---")
    # Q1: Average PM2.5 of Adyar in October
    q1 = cur.execute(
        """SELECT ROUND(AVG(r.pm25), 2) FROM readings r
           JOIN stations s ON r.station_id = s.station_id
           WHERE s.station_name = ? AND r.obs_date LIKE '2026-10-%'""",
        ("Adyar",)
    ).fetchone()[0]
    print(f"Q1. Average PM2.5 of Adyar in Oct 2026: {q1} ug/m3")

    # Q2: Top 5 hours with worst NO2 across all stations
    q2 = cur.execute(
        """SELECT s.station_name, r.obs_date, r.obs_hour, r.no2
           FROM readings r JOIN stations s ON r.station_id = s.station_id
           ORDER BY r.no2 DESC LIMIT 5"""
    ).fetchall()
    print("Q2. Top 5 worst NO2 hours:", q2)

    # Q3: Daily summary sample (first 5 rows)
    q3 = cur.execute(
        """SELECT s.station_name, r.obs_date, MIN(r.pm25), MAX(r.pm25), ROUND(AVG(r.pm25), 2), COUNT(*)
           FROM readings r JOIN stations s ON r.station_id = s.station_id
           GROUP BY s.station_name, r.obs_date LIMIT 5"""
    ).fetchall()
    print("Q3. Daily Summary Sample (Station, Date, Min, Max, Mean, Count):")
    for row in q3:
        print("  ", row)

    con.close()

def generate_charts(cleaned_rows):
    df = pd.DataFrame(cleaned_rows, columns=["station", "date", "hour", "pm25", "pm10", "no2", "temp_c", "minmax", "zscore"])

    # Chart 1: Line chart - Monthly PM2.5 Trend
    daily = df.groupby("date")["pm25"].mean()
    plt.figure(figsize=(9, 4))
    plt.plot(daily.index, daily.values, marker="o", color="#1f77b4", linewidth=1.8)
    plt.title("Daily Mean PM2.5 Trend Across City Network (Oct 2026)")
    plt.xlabel("Date")
    plt.ylabel("Mean PM2.5 (ug/m3)")
    plt.xticks(daily.index[::4], rotation=35)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "chart1_monthly_trend.png"), dpi=150)
    plt.close()

    # Chart 2: Bar chart - Station Comparison
    st_mean = df.groupby("station")["pm25"].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 4))
    plt.bar(st_mean.index, st_mean.values, color="#2ca02c")
    plt.title("Mean PM2.5 Concentration by Monitoring Station")
    plt.xlabel("Monitoring Station")
    plt.ylabel("Mean PM2.5 (ug/m3)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "chart2_station_comparison.png"), dpi=150)
    plt.close()

    # Chart 3: Scatter plot - Temperature vs PM2.5
    plt.figure(figsize=(7, 4.5))
    plt.scatter(df["temp_c"], df["pm25"], alpha=0.5, color="#d62728", edgecolors="none")
    plt.title("Ambient Temperature (C) vs PM2.5 Concentration")
    plt.xlabel("Temperature (Celsius)")
    plt.ylabel("PM2.5 (ug/m3)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "chart3_temp_vs_pm25.png"), dpi=150)
    plt.close()

    # Chart 4: Box plot - Hourly PM2.5 Distribution
    hours = sorted(df["hour"].unique())
    hourly_data = [df[df["hour"] == h]["pm25"].values for h in hours]
    plt.figure(figsize=(8, 4.5))
    plt.boxplot(hourly_data, labels=[f"{h:02d}:00" for h in hours], patch_artist=True)
    plt.title("PM2.5 Distribution by Hour of Day")
    plt.xlabel("Hour of Day")
    plt.ylabel("PM2.5 (ug/m3)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "chart4_hourly_boxplot.png"), dpi=150)
    plt.close()

def benchmark_csv_vs_pandas():
    print("\n--- Alternative Concept Benchmark: Python csv+loops vs Pandas Vectorised ---")
    for n in [1000, 100000, 1000000]:
        # Synthesize n rows in memory
        data = [("Adyar", "2026-10-01", str(round(random.uniform(10, 200), 2))) for _ in range(n)]
        # Method 1: Python loops
        tracemalloc.start()
        t0 = time.perf_counter()
        vals = [float(r[2]) for r in data if r[2] not in ("", "NA") and 0 <= float(r[2]) <= 999]
        lo, hi = min(vals), max(vals)
        norm = [(v - lo) / (hi - lo) for v in vals]
        t_py = time.perf_counter() - t0
        _, peak_py = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Method 2: Pandas vectorised
        df = pd.DataFrame(data, columns=["station", "date", "pm25"])
        tracemalloc.start()
        t0 = time.perf_counter()
        s = pd.to_numeric(df["pm25"], errors="coerce")
        s = s[(s >= 0) & (s <= 999)].dropna()
        norm_pd = (s - s.min()) / (s.max() - s.min())
        t_pd = time.perf_counter() - t0
        _, peak_pd = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Rows={n:7d} | Python Loop: {t_py*1000:7.2f} ms (PyHeap: {peak_py/1e6:5.2f} MB) | Pandas: {t_pd*1000:7.2f} ms (PyHeap: {peak_pd/1e6:5.2f} MB)")

if __name__ == "__main__":
    create_sample_raw_csv()
    with open(RAW_CSV, "r", encoding="utf-8") as f:
        raw_lines = [next(f).strip() for _ in range(9)]
    print("--- B1.1 Before Cleaning (First 8 Data Rows) ---")
    for line in raw_lines:
        print(" ", line)

    cleaned = clean_pipeline(RAW_CSV)
    print("\n--- B1.1 After Cleaning (First 6 Validated Rows) ---")
    for row in cleaned[:6]:
        print(" ", row)

    load_to_sqlite(cleaned)
    generate_charts(cleaned)
    benchmark_csv_vs_pandas()
