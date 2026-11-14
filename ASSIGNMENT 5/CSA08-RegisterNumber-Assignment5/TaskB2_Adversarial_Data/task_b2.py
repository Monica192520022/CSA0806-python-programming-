import csv
import io
import sqlite3
import time

# 1. Adversarial CSV Inputs
def safe_ingest_csv(raw_bytes, encoding="utf-8"):
    try:
        text = raw_bytes.decode(encoding)
    except UnicodeDecodeError as e:
        return f"Handled UnicodeDecodeError: {e}"

    if not text.strip():
        return "Handled Empty File: 0 rows ingested."

    # Check delimiter
    first_line = text.splitlines()[0]
    if "," not in first_line and ";" in first_line:
        return "Handled Wrong Delimiter: semicolon ';' detected instead of comma ','."

    reader = csv.DictReader(io.StringIO(text))
    required_cols = {"station", "date", "pm25"}
    if not reader.fieldnames or not required_cols.issubset(set(reader.fieldnames)):
        return f"Handled Missing Column: found {reader.fieldnames}, expected {sorted(required_cols)}."

    rows = list(reader)
    return f"Successfully parsed {len(rows)} rows."

print("--- B2.1 Adversarial CSV Tests ---")
print("1. Missing Column :", safe_ingest_csv(b"station,date\nAdyar,2026-10-01\n"))
print("2. Wrong Delimiter:", safe_ingest_csv(b"station;date;pm25\nAdyar;2026-10-01;48.0\n"))
print("3. Wrong Encoding :", safe_ingest_csv("Adyar,2026-10-01,48.0°C".encode("latin-1"), encoding="utf-8"))
print("4. Empty File     :", safe_ingest_csv(b""))

# 2. SQL Injection: String Concatenation vs Parameterised Query (?)
print("\n--- B2.2 SQL Injection Test ---")
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?, ?, ?)", [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0)
])
con.commit()

malicious_input = "Adyar' OR '1'='1"

# Vulnerable string concatenation
unsafe_sql = "SELECT * FROM aq WHERE station = '" + malicious_input + "'"
print("Unsafe (+) Query :", unsafe_sql)
print("Unsafe (+) Result:", con.execute(unsafe_sql).fetchall())

# Safe parameterised query
safe_result = con.execute("SELECT * FROM aq WHERE station = ?", (malicious_input,)).fetchall()
print("Safe (?) Result  :", safe_result)

# Alternative Concept Benchmark: executemany() vs execute() in loop
n_test = 50000
sample_batch = [("Adyar", "2026-10-01", 50.0) for _ in range(n_test)]

con.execute("CREATE TABLE bench1 (station TEXT, day TEXT, pm25 REAL)")
t0 = time.perf_counter()
for row in sample_batch:
    con.execute("INSERT INTO bench1 VALUES (?, ?, ?)", row)
con.commit()
t_loop = time.perf_counter() - t0

con.execute("CREATE TABLE bench2 (station TEXT, day TEXT, pm25 REAL)")
t0 = time.perf_counter()
con.executemany("INSERT INTO bench2 VALUES (?, ?, ?)", sample_batch)
con.commit()
t_many = time.perf_counter() - t0
print(f"Insert {n_test} rows -> execute() loop: {t_loop*1000:.2f} ms | executemany(): {t_many*1000:.2f} ms")
con.close()

# 3. Adversarial NLP Sentences for Lexicon Sentiment Scorer
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for i, w in enumerate(words):
        val = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if val != 0 and i > 0 and words[i - 1] in NEGATORS:
            val = -val
        total += val
    return total

def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"

print("\n--- B2.3 Adversarial Sentiment Edge Cases ---")
adversarial_sentences = [
    ("Sarcasm", "Oh great, thick black smoke everywhere, truly clean and helpful!"),
    ("Double Negative", "The air quality is not never bad here."),
    ("Distant Negator", "The sensor was not at all working and remained broken."),
    ("Mixed Opinion", "The app is fast and helpful, but the air is dirty with smoke.")
]
for case_type, sent in adversarial_sentences:
    print(f"[{case_type:15}] Score={score(sent):+d} | Label={label(sent):8} | '{sent}'")
