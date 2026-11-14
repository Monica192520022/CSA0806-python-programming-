# pipeline.py - clean all station files, store in SQLite, answer three questions
import os
import sqlite3
from clean import clean_file

if os.path.exists("airquality.db"):
    os.remove("airquality.db")
con = sqlite3.connect("airquality.db")
con.execute("""CREATE TABLE stations (
                   station_id INTEGER PRIMARY KEY,
                   name TEXT UNIQUE NOT NULL,
                   temp_unit_in_source TEXT)""")
con.execute("""CREATE TABLE readings (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   station_id INTEGER NOT NULL,
                   day TEXT NOT NULL,
                   hour INTEGER NOT NULL,
                   pm25 REAL, pm10 REAL, no2 REAL, temp_c REAL,
                   UNIQUE (station_id, day, hour),
                   FOREIGN KEY (station_id) REFERENCES stations(station_id))""")

for number, name in enumerate(["Adyar", "Guindy", "Velachery", "Perungudi"], start=1):
    unit = "F" if name in ("Guindy", "Perungudi") else "C"
    con.execute("INSERT INTO stations VALUES (?, ?, ?)", (number, name, unit))
    rows, log = clean_file("data/raw_" + name + ".csv")
    data = [(number, r["day"], r["hour"], r["pm25"], r["pm10"], r["no2"], r["temp"]) for r in rows]
    con.executemany("INSERT INTO readings (station_id, day, hour, pm25, pm10, no2, temp_c) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    print(name, "loaded", len(data), "rows | problems:", log)
con.commit()

print("\nQ1 Average PM2.5 of Adyar in October:")
q1 = """SELECT ROUND(AVG(r.pm25), 1) FROM readings r JOIN stations s ON r.station_id = s.station_id
        WHERE s.name = ? AND r.day LIKE '2026-10-%'"""
print(" ", con.execute(q1, ("Adyar",)).fetchone()[0])

print("Q2 Station with the highest average PM2.5:")
q2 = """SELECT s.name, ROUND(AVG(r.pm25), 1) AS avg_pm FROM readings r
        JOIN stations s ON r.station_id = s.station_id GROUP BY s.name ORDER BY avg_pm DESC"""
for row in con.execute(q2):
    print(" ", row)

print("Q3 Hours with the worst air (average PM2.5 over all stations, top 4):")
q3 = "SELECT hour, ROUND(AVG(pm25), 1) AS a FROM readings GROUP BY hour ORDER BY a DESC LIMIT 4"
for row in con.execute(q3):
    print(" ", row)
con.close()
