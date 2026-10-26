"""Task 2 - Alternative concept: integer paise, float+round, Decimal."""
import random
import sys
import time
from decimal import Decimal


def total_int_paise(items):
    """Parse 'rupees.paise' text into an integer number of paise and add ints."""
    total = 0
    for a in items:
        rupees, _, paise = a.partition(".")
        total += int(rupees) * 100 + int(paise.ljust(2, "0")[:2])
    return total


def total_float_plain(items):
    """Plain += loop (Python 3.12's built-in sum() uses compensated summation, which hides the error)."""
    total = 0.0
    for a in items:
        total += float(a)
    return total


def total_float_round_each(items):
    total = 0.0
    for a in items:
        total = round(total + float(a), 2)
    return total


def total_decimal(items):
    total = Decimal("0")
    for a in items:
        total += Decimal(a)
    return total


def as_rupees(paise):
    return f"{paise // 100}.{paise % 100:02d}"


def best_time(fn, items, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn(items)
        best = min(best, time.perf_counter() - t0)
    return best


def make_payments(n, seed=3):
    rng = random.Random(seed)
    return [f"{rng.randint(10, 400)}.{rng.randint(0, 99):02d}" for _ in range(n)]


print("1) The example of the assignment (1003 payments)")
sample = ["33.40"] * 1000 + ["0.10"] * 3
print("   int paise            :", total_int_paise(sample), "paise =", as_rupees(total_int_paise(sample)))
print("   float, no rounding   :", total_float_plain(sample))
print("   float, round each add:", total_float_round_each(sample))
print("   Decimal              :", total_decimal(sample))

print("\n2) Memory per value (sys.getsizeof, bytes)")
print("   float   33.4        :", sys.getsizeof(33.4))
print("   int     3340        :", sys.getsizeof(3340))
print("   Decimal 33.40       :", sys.getsizeof(Decimal("33.40")))

print("\n3) Exactness and time for n payments (best of 3)")
print(f"{'n':>8} {'method':<22} {'total':>16} {'exact?':>7} {'time (s)':>10}")
for n in (300, 6000, 150000):
    items = make_payments(n)
    exact = total_int_paise(items)
    exact_dec = Decimal(exact) / 100
    for name, fn in (("int paise", total_int_paise),
                     ("float, no rounding", total_float_plain),
                     ("float, round each add", total_float_round_each),
                     ("Decimal", total_decimal)):
        value = fn(items)
        shown = as_rupees(value) if name == "int paise" else repr(value) if isinstance(value, float) else str(value)
        if name == "int paise":
            ok = True
        elif isinstance(value, float):
            ok = (Decimal(repr(value)) == exact_dec)
        else:
            ok = (value == exact_dec)
        print(f"{n:>8} {name:<22} {shown:>16} {str(ok):>7} {best_time(fn, items):>10.5f}")
    print()
print("exact? = identical to the integer-paise total (the reference).")
