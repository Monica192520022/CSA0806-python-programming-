# adversarial.py - Task B2: bad files, SQL quote, tricky sentences
import sqlite3
from clean import clean_file
from sentiment import score, label

HEADER = "station,date,hour,pm25,pm10,no2,temp\n"


def safe_clean(path):
    """Try utf-8, then latin-1; report every problem instead of crashing."""
    try:
        try:
            rows, log = clean_file(path)
        except UnicodeDecodeError:
            print("   utf-8 failed, trying latin-1")
            import clean as c
            text = open(path, encoding="latin-1").read()
            open(path + ".utf8", "w", encoding="utf-8").write(text)
            rows, log = clean_file(path + ".utf8")
        print("   OK:", len(rows), "rows read")
    except FileNotFoundError:
        print("   file not found")
    except ValueError as e:
        print("   rejected:", e)


print("1. missing column (no2 removed)")
open("bad_column.csv", "w").write("station,date,hour,pm25,pm10,temp\nAdyar,2026-10-01,8,48,90,30\n")
safe_clean("bad_column.csv")

print("2. wrong delimiter (semicolon)")
open("bad_delim.csv", "w").write(HEADER.replace(",", ";") + "Adyar;2026-10-01;8;48;90;30;30.5\n")
safe_clean("bad_delim.csv")

print("3. different encoding (latin-1 with the letter e-acute)")
open("bad_encoding.csv", "wb").write((HEADER + "Caf\xe9 Road,2026-10-01,8,48,90,30,30.5\n").encode("latin-1"))
safe_clean("bad_encoding.csv")

print("4. empty file")
open("empty.csv", "w").close()
safe_clean("empty.csv")

print("\nSQL with a quote in the station name")
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?, ?)", [("O'Brien Road", 70.0), ("Adyar", 48.0)])
name = "O'Brien Road"
try:
    sql = "SELECT AVG(pm25) FROM aq WHERE station = '" + name + "'"    # string joined with +
    print("  with +      :", con.execute(sql).fetchone())
except sqlite3.OperationalError as e:
    print("  with +      : ERROR ->", e)
print("  with ?      :", con.execute("SELECT AVG(pm25) FROM aq WHERE station = ?", (name,)).fetchone()[0])
evil = "x' OR '1'='1"
sql = "SELECT COUNT(*) FROM aq WHERE station = '" + evil + "'"
print("  injection with + returns", con.execute(sql).fetchone()[0], "rows (should be 0)")
print("  injection with ? returns", con.execute("SELECT COUNT(*) FROM aq WHERE station = ?", (evil,)).fetchone()[0], "rows")

print("\nTricky sentences for the sentiment scorer")
tests = [
    ("Oh good, the water is dirty again.", "negative (sarcasm)"),
    ("The staff are not never helpful.", "positive (double negative)"),
    ("The air is clean but the water is dirty.", "mixed"),
    ("I cannot say the service is good.", "negative"),
    ("Not bad at all.", "positive"),
    ("The bus was not very helpful.", "negative"),
]
for text, truth in tests:
    print("  ", label(text).ljust(8), "(score", score(text), ") expected:", truth.ljust(26), "|", text)
