# clean.py - cleaning rules for one station CSV file (student level)
import csv
from datetime import datetime

FAHRENHEIT_STATIONS = ["Guindy", "Perungudi"]      # these two stations send temperature in F
COLUMNS = ["station", "date", "hour", "pm25", "pm10", "no2", "temp"]
LIMITS = {"pm25": (0, 999), "pm10": (0, 999), "no2": (0, 999), "temp": (-10, 60)}   # valid range


def clean_station(name):
    return name.strip().title()                    # ' adyar ' -> 'Adyar'


def clean_date(text):
    text = text.strip()
    for form in ("%Y-%m-%d", "%d/%m/%Y"):          # two date styles are accepted
        try:
            return datetime.strptime(text, form).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None                                    # date could not be understood


def to_number(text):
    text = text.strip()
    if text == "" or text.upper() == "NA":
        return None                                # missing
    try:
        return float(text)
    except ValueError:
        return None                                # not a number, for example 'abc'


def clean_file(path):
    """Return (rows, log). rows is a list of dictionaries, log counts every problem found."""
    log = {"missing": 0, "impossible": 0, "duplicates": 0, "fahrenheit": 0,
           "filled": 0, "dropped": 0, "bad_date": 0}
    rows = []
    seen = set()
    last_value = {}                                # (station, column) -> last good value

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("the file is empty")
        for col in COLUMNS:
            if col not in reader.fieldnames:
                raise ValueError("missing column: " + col)

        for r in reader:
            station = clean_station(r["station"])
            day = clean_date(r["date"])
            if day is None:
                log["bad_date"] += 1
                continue
            hour = int(float(r["hour"]))

            key = (station, day, hour)
            if key in seen:                        # rule: duplicate row -> keep the first
                log["duplicates"] += 1
                continue
            seen.add(key)

            row = {"station": station, "day": day, "hour": hour}
            for col in ["pm25", "pm10", "no2", "temp"]:
                value = to_number(r[col])
                if value is None:
                    log["missing"] += 1
                elif col == "temp" and station in FAHRENHEIT_STATIONS:
                    value = round((value - 32) * 5 / 9, 1)      # F -> C
                    log["fahrenheit"] += 1
                if value is not None:
                    low, high = LIMITS[col]
                    if value < low or value > high:             # rule: impossible -> missing
                        log["impossible"] += 1
                        value = None
                if value is None and (station, col) in last_value:
                    value = last_value[(station, col)]          # rule: forward fill
                    log["filled"] += 1
                if value is not None:
                    last_value[(station, col)] = value
                row[col] = value

            if row["pm25"] is None:                # still no PM2.5: the row is useless
                log["dropped"] += 1
                continue
            rows.append(row)
    return rows, log


def min_max(values):
    low, high = min(values), max(values)
    return [round((v - low) / (high - low), 3) for v in values]


def z_score(values):
    mean = sum(values) / len(values)
    sd = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
    return [round((v - mean) / sd, 3) for v in values]


if __name__ == "__main__":
    print("BEFORE:")
    print(open("messy.csv").read())
    rows, log = clean_file("messy.csv")
    print("AFTER:")
    for r in rows:
        print(r)
    print("PROBLEMS FOUND:", log)
    pm = [r["pm25"] for r in rows]
    print("min-max :", min_max(pm))
    print("z-score :", z_score(pm))
