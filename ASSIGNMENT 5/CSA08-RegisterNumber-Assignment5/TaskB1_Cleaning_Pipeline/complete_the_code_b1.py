import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""


def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    # TODO 1: Read the text with csv.DictReader; skip rows whose pm25 is empty, 'NA' or
    #   negative; convert pm25 to float
    reader = csv.DictReader(io.StringIO(text.strip()))
    for r in reader:
        val_str = r["pm25"].strip()
        if not val_str or val_str.upper() == "NA":
            continue
        val = float(val_str)
        if val < 0:
            continue
        rows.append((r["station"].strip(), r["date"].strip(), val))
    return rows


def min_max(values):
    # TODO 2: Scale each value to the range 0-1 using (v - min) / (max - min), rounded
    #   to 3 decimals
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [round((v - lo) / (hi - lo), 3) for v in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))

# Extended check: skip rows whose pm25 is above 999
def load_clean_extended(text):
    rows = []
    reader = csv.DictReader(io.StringIO(text.strip()))
    for r in reader:
        val_str = r["pm25"].strip()
        if not val_str or val_str.upper() == "NA":
            continue
        val = float(val_str)
        if val < 0 or val > 999:
            continue
        rows.append((r["station"].strip(), r["date"].strip(), val))
    return rows

RAW_WITH_SPIKE = RAW + "Taramani,2026-10-04,1450\n"
print("With >999 filter:", load_clean_extended(RAW_WITH_SPIKE))
