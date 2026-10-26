"""Task 1 - Understand the problem and identify the data.

Prints the data dictionary, constants, rules and assumptions, then measures the
alternative design (three separate variables per farmer vs one tuple per entry).
"""
import random
import textwrap
import time


def show(title, rows, headers):
    print("=" * 78)
    print(title)
    print("=" * 78)
    for row in rows:
        print("-", " | ".join(f"{h}: {v}" for h, v in zip(headers, row)))
    print()


# ---- 1. inputs and outputs --------------------------------------------------
INPUTS_OUTPUTS = [
    ("farmer_id", "input", "str", "'F001'",
     "An identifier, never used in arithmetic, may have leading zeros -> text"),
    ("shift", "input", "str", "'M' or 'E'",
     "Morning/evening label; two possible values; text"),
    ("litres", "input", "Decimal (fractional)", "8.5",
     "A measured quantity; fractional, so not int"),
    ("fat", "input", "Decimal (fractional)", "4.2",
     "Percentage with 1 decimal (2 decimals with the analyser)"),
    ("snf", "input", "Decimal (fractional)", "8.7",
     "Percentage with 1 decimal (2 decimals with the analyser)"),
    ("rate", "output", "Decimal, 2 places", "33.40",
     "Rupees per litre; must be exact to the paisa"),
    ("amount", "output", "Decimal, 2 places", "283.90",
     "litres x rate, rounded once to the paisa; this is what the bank pays"),
    ("ten_day_total", "output", "Decimal, 2 places", "1593.23",
     "Sum of the rounded amounts of one farmer; paid every ten days"),
    ("entry_count", "derived", "int (whole number)", "20",
     "A count of entries; whole numbers only"),
]
show("DATA DICTIONARY", INPUTS_OUTPUTS, ["name", "role", "type", "example", "why"])

# ---- 2. constants -----------------------------------------------------------
CONSTANTS = [
    ("BASE_RATE", "30.00", "Rs/litre for standard milk; changes only by revision"),
    ("FAT_STEP_VALUE", "0.40", "Rs/litre for each 0.1 % of fat from standard"),
    ("SNF_STEP_VALUE", "0.30", "Rs/litre for each 0.1 % of SNF from standard"),
    ("STD_FAT", "3.5", "Reference fat %"),
    ("STD_SNF", "8.5", "Reference SNF %"),
    ("STEP", "0.1", "Size of one fat/SNF step in %"),
    ("MIN_FAT / MAX_FAT", "2.0 / 7.0", "Allowed fat range given in the assignment"),
    ("MIN_SNF / MAX_SNF", "7.0 / 10.0", "ASSUMED SNF range (not given)"),
    ("MAX_LITRES", "500", "ASSUMED upper limit of one entry (catches typing errors)"),
]
show("NAMED CONSTANTS (never change during a run)", CONSTANTS,
     ["name", "value", "why a constant"])

# ---- 3. rules ---------------------------------------------------------------
RULES = [
    ("R1", "litres > 0 and litres <= MAX_LITRES",
     "A negative or zero quantity would reduce or cancel a payment"),
    ("R2", "MIN_FAT <= fat <= MAX_FAT (2.0 .. 7.0)",
     "Outside this range milk is not buffalo/cow milk -> typing or machine error"),
    ("R3", "MIN_SNF <= snf <= MAX_SNF", "Same reason as R2 for SNF"),
    ("R4", "every input must be a finite number", "'eight', '8,5', 'nan' must be rejected"),
    ("R5", "amount has exactly 2 decimals", "The bank statement is in paise"),
    ("R6", "ten_day_total == sum of the rounded amounts",
     "Otherwise the total differs from the bank statement by a few paise"),
]
show("RULES EVERY CORRECT PAYMENT MUST SATISFY", RULES, ["rule", "condition", "why"])

ASSUMPTIONS = [
    "SNF must lie between 7.0 and 10.0 (the assignment only fixes the fat range).",
    "One entry is at most 500 litres.",
    "A step is rounded to the NEAREST whole 0.1 % (assignment: 'every 0.1 %').",
    "Half a paisa is rounded up (ROUND_HALF_UP), as banks do.",
    "Each payment is rounded to the paisa first; the ten-day total is the sum of those.",
]
print("ASSUMPTIONS")
for a in ASSUMPTIONS:
    print(textwrap.fill("* " + a, 78, subsequent_indent="  "))
print()


# ---- 4. alternative concept: three separate variables vs one tuple ----------
def rate(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40
                 + round((snf - 8.5) / 0.1) * 0.30, 2)


def make_entries(n, seed=7):
    rng = random.Random(seed)
    return [(round(rng.uniform(2, 30), 1), round(rng.uniform(2.5, 5.5), 1),
             round(rng.uniform(7.5, 9.5), 1)) for _ in range(n)]


def separate_variable_source(entries):
    """Builds the program text that the 'litres1, fat1, snf1 ...' design needs."""
    lines = []
    for i, (l, f, s) in enumerate(entries, start=1):
        lines += [f"litres{i} = {l}", f"fat{i} = {f}", f"snf{i} = {s}"]
    lines.append("total = 0.0")
    for i in range(1, len(entries) + 1):
        lines.append(f"total += litres{i} * rate(fat{i}, snf{i})")
    return "\n".join(lines)


def total_with_loop(entries):
    total = 0.0
    for litres, fat, snf in entries:
        total += litres * rate(fat, snf)
    return total


print("=" * 78)
print("ALTERNATIVE: separate variables per entry vs one tuple per entry in a list")
print("=" * 78)
print(f"{'n':>8} {'design':<20} {'source lines':>13} {'source chars':>13} {'time (s)':>10}")
for n in (300, 6000):
    entries = make_entries(n)
    src = separate_variable_source(entries)
    t0 = time.perf_counter()
    ns = {"rate": rate}
    exec(compile(src, "<separate>", "exec"), ns)
    t1 = time.perf_counter()
    print(f"{n:>8} {'separate variables':<20} {src.count(chr(10)) + 1:>13} {len(src):>13} {t1 - t0:>10.4f}")
    t0 = time.perf_counter()
    loop_total = total_with_loop(entries)
    t1 = time.perf_counter()
    print(f"{n:>8} {'list of tuples':<20} {'6 (fixed)':>13} {'~150 (fixed)':>13} {t1 - t0:>10.4f}")
    assert abs(ns["total"] - loop_total) < 1e-6
print(f"{150000:>8} {'separate variables':<20} {'600,001':>13} {'not attempted':>13}")
t0 = time.perf_counter()
total_with_loop(make_entries(150000))
print(f"{150000:>8} {'list of tuples':<20} {'6 (fixed)':>13} {'~150 (fixed)':>13} {time.perf_counter() - t0:>10.4f}")
print("\nBoth designs give the same total (asserted), but the program TEXT of the")
print("first design grows with n, because every new farmer needs new variable names.")
