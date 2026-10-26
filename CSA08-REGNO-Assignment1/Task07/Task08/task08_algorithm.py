"""Task 8 - Algorithm: hand trace, store-then-add vs running total."""
import random
import time
import tracemalloc
from decimal import Decimal, ROUND_HALF_UP

BASE, FAT_V, SNF_V = Decimal("30.00"), Decimal("0.40"), Decimal("0.30")
PAISA = Decimal("0.01")


def steps(value, standard):
    return ((value - standard) / Decimal("0.1")).quantize(Decimal("1"), ROUND_HALF_UP)


def payment(litres, fat, snf):
    rate = (BASE + steps(fat, Decimal("3.5")) * FAT_V + steps(snf, Decimal("8.5")) * SNF_V).quantize(PAISA)
    return rate, (litres * rate).quantize(PAISA, ROUND_HALF_UP)


print("1) Hand trace of the pseudocode for three entries (compare with Task08/pseudocode.md)")
entries = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3")]
total = Decimal("0.00")
print(f"   {'i':>2} {'litres':>7} {'fat':>5} {'snf':>5} {'fat_steps':>9} {'snf_steps':>9} {'rate':>7} {'amount':>8} {'total':>9}")
for i, (l, f, s) in enumerate(entries, start=1):
    l, f, s = Decimal(l), Decimal(f), Decimal(s)
    fs, ss = steps(f, Decimal("3.5")), steps(s, Decimal("8.5"))
    rate, amount = payment(l, f, s)
    total += amount
    print(f"   {i:>2} {l:>7} {f:>5} {s:>5} {fs:>9} {ss:>9} {rate:>7} {amount:>8} {total:>9}")
print("   ten_day_total =", total)


def make_entries(n, seed=5):
    rng = random.Random(seed)
    for _ in range(n):
        yield (Decimal(rng.randint(200, 3000)) / 10, Decimal(rng.randint(25, 60)) / 10,
               Decimal(rng.randint(75, 95)) / 10)


def total_store_then_add(n):
    amounts = []                         # O(n) space
    for l, f, s in make_entries(n):
        amounts.append(payment(l, f, s)[1])
    return sum(amounts, Decimal("0.00"))


def total_running(n):
    total = Decimal("0.00")              # O(1) space
    for l, f, s in make_entries(n):
        total += payment(l, f, s)[1]
    return total


print("\n2) ALTERNATIVE: store every amount in a list, or keep a running total")
print(f"   {'n':>8} {'method':<18} {'total':>14} {'time (s)':>9} {'peak memory (KB)':>17}")
for n in (300, 6000, 150000):
    for name, fn in (("store then add", total_store_then_add), ("running total", total_running)):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = fn(n)
        elapsed = time.perf_counter() - t0
        peak = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()
        print(f"   {n:>8} {name:<18} {result:>14} {elapsed:>9.4f} {peak:>17.1f}")
print("   Same total, same O(n) time; peak memory grows with n only for 'store then add'.")
print("   Storing is still needed when the amounts must be printed again, sorted, or audited.")
