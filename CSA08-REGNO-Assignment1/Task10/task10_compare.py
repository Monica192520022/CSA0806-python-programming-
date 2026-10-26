"""Task 10 - float vs Decimal, rounding rules, timing, and the rate-table alternative."""
import random
import sys
import time
from decimal import Decimal, ROUND_HALF_UP

from calculator import PAISA, payout, rate_per_litre


def make_entries(n, seed=2025):
    rng = random.Random(seed)
    return [(Decimal(rng.randint(200, 3500)) / 100,      # 2.00 .. 35.00 litres
             Decimal(rng.randint(25, 60)) / 10,           # fat 2.5 .. 6.0
             Decimal(rng.randint(75, 95)) / 10)           # snf 7.5 .. 9.5
            for _ in range(n)]


def rate_float(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)


def total_decimal_each(entries):                 # A: reference (what the bank pays)
    total = Decimal("0.00")
    for l, f, s in entries:
        total += payout(l, f, s)
    return total


def total_decimal_once(entries):                 # B: round only the total
    total = Decimal("0")
    for l, f, s in entries:
        total += l * rate_per_litre(f, s)
    return total.quantize(PAISA, ROUND_HALF_UP)


def total_float_each(entries):                   # C: float, every payment rounded
    total = 0.0
    for l, f, s in entries:
        total += round(float(l) * rate_float(float(f), float(s)), 2)
    return total


def total_float_once(entries):                   # D: float, only total rounded
    total = 0.0
    for l, f, s in entries:
        total += float(l) * rate_float(float(f), float(s))
    return round(total, 2)


def timed(fn, entries):
    t0 = time.perf_counter()
    result = fn(entries)
    return result, time.perf_counter() - t0


print("1) Totals (A is the reference: Decimal, each payment rounded once to the paisa)")
print(f"{'n':>8} | {'A Decimal each':>16} | {'B Decimal once':>16} {'B-A':>7} | {'C float each (raw)':>22} {'C-A':>12} | {'D float once':>16} {'D-A':>7}")
rows = []
for n in (300, 6000, 150000):
    entries = make_entries(n)
    a, ta = timed(total_decimal_each, entries)
    b, tb = timed(total_decimal_once, entries)
    c, tc = timed(total_float_each, entries)
    d, td = timed(total_float_once, entries)
    rows.append((n, ta, tb, tc, td))
    print(f"{n:>8} | {a:>16} | {b:>16} {b - a:>7} | {c!r:>22} {Decimal(c) - a:>12.2E} | {d:>16} {Decimal(str(d)) - a:>7}")
    print(f"{'':>8}   round(C,2) == A ? {Decimal(str(round(c, 2))) == a}")

print("\n2) How many single payments differ between float round() and Decimal ROUND_HALF_UP?")
for n in (300, 6000, 150000):
    entries = make_entries(n)
    diff = sum(1 for l, f, s in entries
               if Decimal(str(round(float(l) * rate_float(float(f), float(s)), 2))) != payout(l, f, s))
    print(f"   n = {n:>6}: {diff} payments differ by one paisa")

print("\n3) Time to compute (seconds, one run)")
print(f"{'n':>8} {'Decimal each':>13} {'Decimal once':>13} {'float each':>11} {'float once':>11}")
for n, ta, tb, tc, td in rows:
    print(f"{n:>8} {ta:>13.4f} {tb:>13.4f} {tc:>11.4f} {td:>11.4f}")

print("\n4) ALTERNATIVE: rate table (dictionary) instead of recalculating every entry")
entries = make_entries(150000)
distinct = {(f, s) for _, f, s in entries}
print(f"   distinct (fat, snf) pairs in 150,000 entries: k = {len(distinct)}")


def total_recalc(entries):
    total = Decimal("0.00")
    for l, f, s in entries:
        total += payout(l, f, s)
    return total


def build_table():
    fats = [Decimal(i) / 10 for i in range(20, 71)]      # 2.0 .. 7.0
    snfs = [Decimal(i) / 10 for i in range(70, 101)]     # 7.0 .. 10.0
    return {(f, s): rate_per_litre(f, s) for f in fats for s in snfs}


def total_table(entries, table):
    total = Decimal("0.00")
    for l, f, s in entries:
        total += (l * table[(f, s)]).quantize(PAISA, ROUND_HALF_UP)
    return total


def best(fn, *args):
    b = 1e9
    for _ in range(3):
        t0 = time.perf_counter()
        r = fn(*args)
        b = min(b, time.perf_counter() - t0)
    return r, b


t0 = time.perf_counter()
table = build_table()
build = time.perf_counter() - t0
r1, t_recalc = best(total_recalc, entries)
r2, t_table = best(total_table, entries, table)
print(f"   full table (all {len(table)} allowed pairs) built in {build:.4f} s, dict size {sys.getsizeof(table)} bytes")
print(f"   recalculate each entry : {t_recalc:.4f} s  total {r1}")
print(f"   dictionary lookup      : {t_table:.4f} s  total {r2}")
print(f"   same total? {r1 == r2}   speed-up x{t_recalc / t_table:.2f}")
