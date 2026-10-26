"""Task 9 - tests with assert statements and a printed test table."""
from decimal import Decimal as D

from calculator import payout, rate_per_litre, ten_day_total, validate_entry

VALID = [
    # id,  description,                  litres, fat,   snf,   rate,    amount
    ("N1", "standard milk",              "10",   "3.5", "8.5", "30.00", "300.00"),
    ("N2", "fat above standard",         "8.5",  "4.2", "8.5", "32.80", "278.80"),
    ("N3", "fat below standard",         "10",   "3.1", "8.5", "28.40", "284.00"),
    ("N4", "SNF above standard",         "10",   "3.5", "8.9", "31.20", "312.00"),
    ("N5", "SNF below standard",         "10",   "3.5", "8.1", "28.80", "288.00"),
    ("N6", "fat and SNF above",          "8.5",  "4.2", "8.7", "33.40", "283.90"),
    ("N7", "fat and SNF below",          "12",   "3.1", "8.3", "27.80", "333.60"),
    ("B1", "boundary: lowest fat 2.0",   "10",   "2.0", "8.5", "24.00", "240.00"),
    ("B2", "boundary: highest fat 7.0",  "10",   "7.0", "8.5", "44.00", "440.00"),
    ("B3", "boundary: lowest SNF 7.0",   "10",   "3.5", "7.0", "25.50", "255.00"),
    ("B4", "boundary: highest SNF 10.0", "10",   "3.5", "10.0", "34.50", "345.00"),
    ("B5", "half-paisa rounds up",       "7.25", "3.0", "8.0", "26.50", "192.13"),
]
INVALID = [
    ("I1", "text instead of litres", "abc", "3.5", "8.5"),
    ("I2", "negative litres",        "-5",  "3.5", "8.5"),
    ("I3", "zero litres",            "0",   "3.5", "8.5"),
    ("I4", "litres too large",       "501", "3.5", "8.5"),
    ("I5", "fat below 2.0",          "10",  "1.9", "8.5"),
    ("I6", "fat above 7.0",          "10",  "7.1", "8.5"),
    ("I7", "fat typed as 'eight'",   "10",  "eight", "8.5"),
    ("I8", "comma decimal '8,5'",    "10",  "3.5", "8,5"),
    ("I9", "SNF below 7.0",          "10",  "3.5", "6.9"),
    ("I10", "nan as fat",            "10",  "nan", "8.5"),
    ("I11", "empty litres",          "",    "3.5", "8.5"),
]

print(f"{'ID':<4}{'Case':<28}{'Input (L, fat, snf)':<24}{'Expected':<20}{'Actual':<20}Result")
print("-" * 106)
failures = 0
for tid, text, l, f, s, exp_rate, exp_amount in VALID:
    litres, fat, snf = validate_entry(l, f, s)
    actual = (rate_per_litre(fat, snf), payout(litres, fat, snf))
    expected = (D(exp_rate), D(exp_amount))
    ok = actual == expected
    failures += not ok
    print(f"{tid:<4}{text:<28}{l + ', ' + f + ', ' + s:<24}"
          f"{exp_rate + ' / ' + exp_amount:<20}{str(actual[0]) + ' / ' + str(actual[1]):<20}{'PASS' if ok else 'FAIL'}")
    assert ok, tid

for tid, text, l, f, s in INVALID:
    try:
        validate_entry(l, f, s)
        ok, actual = False, "accepted"
    except ValueError as err:
        ok, actual = True, "ValueError"
    failures += not ok
    print(f"{tid:<4}{text:<28}{(l or '<empty>') + ', ' + f + ', ' + s:<24}{'ValueError':<20}{actual:<20}{'PASS' if ok else 'FAIL'}")
    assert ok, tid

# ---- 5 entries whose total was calculated by hand ----
hand = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3"),
        ("15.5", "3.8", "8.5"), ("7.25", "3.0", "8.0")]
hand_amounts = [D("300.00"), D("283.90"), D("333.60"), D("483.60"), D("192.13")]
entries = [validate_entry(*e) for e in hand]
actual_amounts = [payout(*e) for e in entries]
hand_total = D("1593.23")   # 300.00 + 283.90 + 333.60 + 483.60 + 192.13
ok = actual_amounts == hand_amounts and ten_day_total(entries) == hand_total
failures += not ok
print(f"{'H1':<4}{'5 entries, total by hand':<28}{'5 entries':<24}{'1593.23':<20}{str(ten_day_total(entries)):<20}{'PASS' if ok else 'FAIL'}")
assert ok

print("-" * 106)
print(f"{len(VALID) + len(INVALID) + 1} test cases, {failures} failures")
assert failures == 0
print("All tests passed.")
