"""Task 5 - Reading input and converting types."""
import builtins
import math
import sys
import timeit


def is_valid_number(text):
    """Check with str methods only; allows an optional leading '-' and one '.'."""
    t = text.strip()
    if t.startswith("-"):
        t = t[1:]
    if t == "" or t.count(".") > 1:
        return False
    return t.replace(".", "", 1).isdecimal()


def parse_try(text):
    """try/except version; also rejects nan and inf, which float() accepts."""
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def read_float(prompt, low, high):
    """Keeps asking until a number between low and high is typed."""
    while True:
        text = input(prompt)
        value = parse_try(text)
        if value is None:
            print(f"   '{text}' is not a number. Use a dot, e.g. 8.5")
        elif not low <= value <= high:
            print(f"   {value} is outside {low} .. {high}")
        else:
            return value


print("1) input() always returns a string")
simulated = iter(["8.5"])
builtins_input = builtins.input
builtins.input = lambda prompt="": next(simulated)
value = input("Enter fat %: ")
builtins.input = builtins_input
print("   typed 8.5 -> value =", repr(value), "type:", type(value).__name__)
print("   value + 1 would fail; float(value) + 1 =", float(value) + 1)
print("   int('8.5') ->", end=" ")
try:
    int("8.5")
except ValueError as err:
    print("ValueError:", err)

print("\n2) Checking input: string methods vs try/except")
print(f"   {'text':<10} {'str methods':>12} {'try/except':>12}")
for text in ("8.5", "8,5", " 8.5 ", "eight", "", "-3", "1e2", "nan", "inf", "8.5.1", "8."):
    print(f"   {text!r:<10} {str(is_valid_number(text)):>12} {str(parse_try(text)):>12}")
print("   '8,5' and 'eight' are rejected by both; ' 8.5 ' is accepted by both (spaces stripped).")
print("   '1e2' is rejected by the str check but accepted by float(); 'nan'/'inf' need math.isfinite.")

print("\n3) Retry loop with simulated typing: 8,5 -> eight -> 9.9 -> 4.2")
answers = iter(["8,5", "eight", "9.9", "4.2"])
builtins.input = lambda prompt="": (print(prompt + (a := next(answers))) or a)
fat = read_float("Fat % (2.0-7.0): ", 2.0, 7.0)
builtins.input = builtins_input
print("   accepted fat =", fat)

print("\n4) Aligned output with f-strings")
rows = [("F001", 10, 3.5, 8.5, 30.00, 300.00), ("F002", 8.5, 4.2, 8.7, 33.40, 283.90),
        ("F003", 12, 3.1, 8.3, 27.80, 333.60)]
print(f"   {'Farmer':<8}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>8}{'Amount':>10}")
for fid, litres, fat, snf, rate, amount in rows:
    print(f"   {fid:<8}{litres:>8.1f}{fat:>6.1f}{snf:>6.1f}{rate:>8.2f}{amount:>10.2f}")
total = sum(r[5] for r in rows)
print(f"   {'TOTAL':<8}{'':>28}{total:>10,.2f}")
print(f"   centred: [{3.5:^10.2f}]   zero padded: [{7.5:08.2f}]   thousands: [{1234567.891:,.2f}]")

print("\n5) ALTERNATIVE timing: valid and invalid text (200,000 repeats)")
for text in ("8.5", "eight"):
    t1 = timeit.timeit(lambda: is_valid_number(text), number=200000)
    t2 = timeit.timeit(lambda: parse_try(text), number=200000)
    print(f"   input {text!r:<8} str methods: {t1:.3f} s   try/except: {t2:.3f} s")

if "--interactive" in sys.argv:
    print("\nInteractive test")
    print("You typed:", read_float("Fat % (2.0-7.0): ", 2.0, 7.0))
