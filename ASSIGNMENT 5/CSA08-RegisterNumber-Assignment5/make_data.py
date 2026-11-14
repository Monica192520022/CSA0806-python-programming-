# make_data.py - creates 4 raw station files for October 2026 with problems on purpose
import csv
import math
import random

random.seed(1)
BASE = {"Adyar": 45, "Guindy": 85, "Velachery": 60, "Perungudi": 70}
IN_FAHRENHEIT = ["Guindy", "Perungudi"]

for station in BASE:
    with open("data/raw_" + station + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["station", "date", "hour", "pm25", "pm10", "no2", "temp"])
        for day in range(1, 32):
            for hour in range(24):
                temp = 27 + 5 * math.sin((hour - 9) * math.pi / 12) + random.uniform(-1, 1)
                rush = 25 if hour in (8, 9, 19, 20) else 0              # rush-hour peaks
                trend = 0.8 * day                                        # air gets worse in the month
                pm25 = BASE[station] + rush + trend - 1.5 * (temp - 27) + random.gauss(0, 6)
                pm10 = pm25 * 1.8 + random.gauss(0, 8)
                no2 = 20 + rush / 2 + random.gauss(0, 4)
                values = [round(pm25, 1), round(pm10, 1), round(no2, 1), round(temp, 1)]
                if station in IN_FAHRENHEIT:
                    values[3] = round(temp * 9 / 5 + 32, 1)
                # put problems in
                if random.random() < 0.03:
                    values[0] = random.choice(["", "NA"])               # missing
                if random.random() < 0.005:
                    values[0] = random.choice([-5, 9999])               # sensor fault
                row = [station, "2026-10-%02d" % day, hour] + values
                w.writerow(row)
                if random.random() < 0.002:
                    w.writerow(row)                                      # duplicate row
