"""Task 12 D - tests for both seasons, two-decimal readings, the bonus and invalid input."""
from decimal import Decimal as D

import milkrate_v2 as m

RATE_CASES = [
    # id, season, mode, litres, fat, snf, expected rate, expected payout
    ("S1", "summer",   "proportional", "10", "3.50", "8.50", "32.00", "320.00"),
    ("S2", "standard", "proportional", "10", "3.50", "8.50", "30.00", "300.00"),
    ("S3", "summer",   "proportional", "10", "4.20", "8.70", "35.75", "357.50"),
    ("S4", "standard", "proportional", "10", "4.20", "8.70", "33.40", "334.00"),
    ("S5", "summer",   "proportional", "10", "3.57", "8.53", "32.41", "324.10"),
    ("S6", "standard", "proportional", "10", "3.57", "8.53", "30.37", "303.70"),
    ("S7", "standard", "nearest",      "10", "3.57", "8.53", "30.40", "304.00"),
    ("S8", "summer",   "proportional", "10", "2.00", "7.00", "20.75", "207.50"),
    ("S9", "summer",   "proportional", "10", "3.45", "8.50", "31.78", "317.80"),
]
INVALID = [
    ("V1", "fat with 3 decimals", ("10", "3.555", "8.5")),
    ("V2", "fat above 7.0",       ("10", "7.01", "8.5")),
    ("V3", "zero litres",         ("0", "3.5", "8.5")),
    ("V4", "text litres",         ("ten", "3.5", "8.5")),
    ("V5", "snf with comma",      ("10", "3.5", "8,5")),
]
BONUS_CASES = [
    # id, season, entries (litres, fat, snf), litres, base, bonus, total
    ("B1", "summer",   [("170", "3.5", "8.5")] * 3, "510", "16320.00", "255.00", "16575.00"),
    ("B2", "summer",   [("250", "3.5", "8.5")] * 2, "500", "16000.00", "0.00", "16000.00"),
    ("B3", "summer",   [("250", "3.5", "8.5"), ("250.1", "3.5", "8.5")], "500.1", "16003.20", "250.05", "16253.25"),
    ("B4", "standard", [("200", "3.5", "8.5")] * 3, "600", "18000.00", "300.00", "18300.00"),
]

failures = 0
print(f"{'ID':<4}{'Season':<10}{'Mode':<13}{'Input (L, fat, snf)':<22}{'Expected rate/pay':<20}{'Actual rate/pay':<20}Result")
print("-" * 95)
for tid, season, mode, l, f, s, e_rate, e_pay in RATE_CASES:
    litres, fat, snf = m.validate_entry(l, f, s)
    a_rate = m.rate_per_litre(fat, snf, season, mode)
    a_pay = m.payout(litres, fat, snf, season, mode)
    ok = (a_rate, a_pay) == (D(e_rate), D(e_pay))
    failures += not ok
    print(f"{tid:<4}{season:<10}{mode:<13}{l + ', ' + f + ', ' + s:<22}{e_rate + '/' + e_pay:<20}{str(a_rate) + '/' + str(a_pay):<20}{'PASS' if ok else 'FAIL'}")
    assert ok, tid

print("\nInvalid readings")
for tid, text, args in INVALID:
    try:
        m.validate_entry(*args)
        ok = False
    except ValueError:
        ok = True
    failures += not ok
    print(f"{tid:<4}{text:<24}{'ValueError expected':<22}{'PASS' if ok else 'FAIL'}")
    assert ok, tid

print("\nSeason by month")
for month, expected in ((1, "standard"), (3, "standard"), (4, "summer"), (5, "summer"),
                        (6, "summer"), (7, "standard"), (12, "standard")):
    ok = m.season_for_month(month) == expected
    failures += not ok
    print(f"   month {month:>2} -> {m.season_for_month(month):<9} {'PASS' if ok else 'FAIL'}")
    assert ok
try:
    m.season_for_month(13)
    failures += 1
except ValueError:
    print("   month 13 -> ValueError PASS")

print("\nTen-day bonus (more than 500 L earns Rs 0.50 per litre on all litres)")
print(f"{'ID':<4}{'Season':<10}{'Litres':>8}{'Base':>12}{'Bonus':>9}{'Total':>12}   Result")
for tid, season, raw, litres_e, base_e, bonus_e, total_e in BONUS_CASES:
    entries = [m.validate_entry(*e) for e in raw]
    r = m.ten_day_summary(entries, season)
    ok = (r["litres"], r["base_amount"], r["bonus"], r["total"]) == (D(litres_e), D(base_e), D(bonus_e), D(total_e))
    failures += not ok
    print(f"{tid:<4}{season:<10}{r['litres']:>8}{r['base_amount']:>12}{r['bonus']:>9}{r['total']:>12}   {'PASS' if ok else 'FAIL'}")
    assert ok, tid

print("-" * 82)
print(f"failures: {failures}")
assert failures == 0
print("All Task 12 tests passed.")
