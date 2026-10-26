"""Task 6 - Functions, scope, and the no-function / lambda alternatives."""
import random
import time

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1


def rate_per_litre(fat, snf):
    """Return the price per litre (float, 2 decimals) for the given fat % and SNF %."""
    fat_steps = round((fat - STD_FAT) / STEP)
    snf_steps = round((snf - STD_SNF) / STEP)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable (float, 2 decimals) for one entry."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(entries):
    """Return the total of all (litres, fat, snf) entries, rounded to 2 decimals."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)


def print_payout(litres, fat, snf):
    """Print (does NOT return) the payout: the result cannot be reused."""
    print("   printed:", payout(litres, fat, snf))


def make_entries(n, seed=11):
    rng = random.Random(seed)
    return [(round(rng.uniform(2, 30), 1), round(rng.uniform(2.5, 5.5), 1),
             round(rng.uniform(7.5, 9.5), 1)) for _ in range(n)]


print("1) Return versus print")
r = payout(8.5, 4.2, 8.7)
print("   returned value can be stored and reused:", r, "-> doubled:", r * 2)
p = print_payout(8.5, 4.2, 8.7)
print("   value stored from the print-only function:", p)

print("\n2) Local and global names")
print("   BASE_RATE is read inside rate_per_litre without 'global' -> OK:", rate_per_litre(3.5, 8.5))


def bad_revision():
    BASE_RATE = 99.0            # creates a NEW local name; the global is untouched
    return BASE_RATE


print("   bad_revision() returns", bad_revision(), "but global BASE_RATE is still", BASE_RATE)


def broken():
    try:
        BASE_RATE += 1          # tries to change a global -> local assumed -> error
    except UnboundLocalError as err:
        return f"UnboundLocalError: {err}"


print("  ", broken())
print("   Rule: read constants inside functions, never change them there.")

print("\n3) Docstrings")
for f in (rate_per_litre, payout, ten_day_total):
    print(f"   {f.__name__}.__doc__ = {f.__doc__}")

print("\n4) The three entries of Task 7 through the functions")
entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
for l, f, s in entries:
    print(f"   {l:>5} L fat {f} snf {s} rate {rate_per_litre(f, s):6.2f} pay {payout(l, f, s):8.2f}")
print("   ten_day_total =", ten_day_total(entries))

# --------------- alternatives: no functions, lambda ---------------
rate_lambda = lambda fat, snf: round(30.0 + round((fat - 3.5) / 0.1) * 0.40
                                     + round((snf - 8.5) / 0.1) * 0.30, 2)
payout_lambda = lambda l, f, s: round(l * rate_lambda(f, s), 2)


def total_no_functions(entries):
    """Script style: the formula is pasted into the loop."""
    total = 0.0
    for l, f, s in entries:
        total += round(l * round(30.0 + round((f - 3.5) / 0.1) * 0.40
                                 + round((s - 8.5) / 0.1) * 0.30, 2), 2)
    return round(total, 2)


def total_lambda(entries):
    total = 0.0
    for l, f, s in entries:
        total += payout_lambda(l, f, s)
    return round(total, 2)


print("\n5) ALTERNATIVE: no functions / lambda  (time for n entries, best of 3)")
print(f"   {'n':>8} {'functions':>11} {'no functions':>13} {'lambda':>9}   same total?")
for n in (300, 6000, 150000):
    data = make_entries(n)
    times = []
    results = []
    for fn in (ten_day_total, total_no_functions, total_lambda):
        best = 1e9
        for _ in range(3):
            t0 = time.perf_counter()
            res = fn(data)
            best = min(best, time.perf_counter() - t0)
        times.append(best)
        results.append(res)
    print(f"   {n:>8} {times[0]:>11.5f} {times[1]:>13.5f} {times[2]:>9.5f}   {len(set(results)) == 1}")
print("   Repeated code: functions = formula written once; no-function script = once per place used.")
