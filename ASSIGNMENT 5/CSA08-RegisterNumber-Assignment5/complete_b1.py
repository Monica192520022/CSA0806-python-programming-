import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,5000
"""


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    # TODO 1
    reader = csv.DictReader(io.StringIO(text))
    for r in reader:
        value = r["pm25"].strip()
        if value == "" or value.upper() == "NA":
            continue
        pm = float(value)
        if pm < 0 or pm > 999:            # extra check: skip negative and above 999
            continue
        rows.append((r["station"], r["date"], pm))
    return rows


def min_max(values):
    # TODO 2
    low = min(values)
    high = max(values)
    return [round((v - low) / (high - low), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
