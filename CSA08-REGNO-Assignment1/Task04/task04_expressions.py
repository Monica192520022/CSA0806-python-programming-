"""Task 4 - Correct expressions, surprises, and the int/floor alternatives."""
import math
import timeit

print("1) Operator precedence and associativity")
for expr in ("2 + 3 * 4", "(2 + 3) * 4", "-2 ** 2", "(-2) ** 2", "2 ** 3 ** 2",
             "(2 ** 3) ** 2", "10 - 4 - 3", "-7 // 2", "not True or True",
             "True or False and False"):
    print(f"   {expr:<26} = {eval(expr)}")

print("\n2) Surprising results (floating point and rounding)")
surprises = [
    ("(4.2 - 3.5) / 0.1", (4.2 - 3.5) / 0.1),
    ("(3.8 - 3.5) / 0.1", (3.8 - 3.5) / 0.1),
    ("int((3.8 - 3.5) / 0.1)", int((3.8 - 3.5) / 0.1)),
    ("round((3.8 - 3.5) / 0.1)", round((3.8 - 3.5) / 0.1)),
    ("0.1 * 3", 0.1 * 3),
    ("1.1 + 2.2", 1.1 + 2.2),
    ("round(2.5), round(3.5)", (round(2.5), round(3.5))),
    ("-2 ** 2", -2 ** 2),
]
for text, value in surprises:
    print(f"   {text:<28} -> {value!r}")
print(f"   (4.2-3.5)/0.1 is {(4.2 - 3.5) / 0.1!r}, not 7 (the assignment quotes 7.000000000000001; the last")
print("   digits depend on the exact subtraction), because 4.2, 3.5 and 0.1 cannot all be")
print("   stored exactly in binary; round() brings the step count back to 7.")
print(f"   (3.8-3.5)/0.1 is {(3.8 - 3.5) / 0.1!r}: int() truncates it to 2 -> a WRONG step count.")
print("   round(2.5)=2 and round(3.5)=4: Python rounds exact halves to the even number.")

print("\n3) round(), int() and math.floor() for negative values")
print(f"   {'x':>6} {'round':>6} {'int':>5} {'floor':>6}")
for x in (-2.5, -2.4, -0.6, -0.4, 0.4, 2.6):
    print(f"   {x:>6} {round(x):>6} {int(x):>5} {math.floor(x):>6}")
print("   int() cuts towards zero, floor() goes down, round() goes to the nearest.")

print("\n4) Comparison chaining and Boolean operators")
fat = 4.2
print("   2.0 <= fat <= 7.0 with fat=4.2 :", 2.0 <= fat <= 7.0)
print("   2.0 <= 7.5 <= 7.0              :", 2.0 <= 7.5 <= 7.0)
print("   1 < 2 < 3 > 2                  :", 1 < 2 < 3 > 2)
litres, snf = 10, 8.5
print("   litres > 0 and 7.0 <= snf <= 10.0 :", litres > 0 and 7.0 <= snf <= 10.0)
print("   short circuit: False and (1/0)  :", False and (1 / 0))

BASE_RATE, FAT_V, SNF_V = 30.00, 0.40, 0.30


def rate_with(method, fat, snf):
    fat_steps = method((fat - 3.5) / 0.1)
    snf_steps = method((snf - 8.5) / 0.1)
    return round(BASE_RATE + fat_steps * FAT_V + snf_steps * SNF_V, 2), fat_steps


print("\n5) The final expression (round-based steps) for the three entries of Task 7")
for fat, snf in ((3.5, 8.5), (4.2, 8.7), (3.1, 8.3)):
    rate, fs = rate_with(round, fat, snf)
    print(f"   fat {fat} snf {snf}: fat_steps = {fs:>3}, rate = {rate:.2f}")

print("\n6) ALTERNATIVE: int() / math.floor() instead of round()  (snf = 8.5)")
print(f"   {'fat':>5} {'exact steps':>12} | {'round':>14} | {'int':>14} | {'floor':>14}")
for fat in (4.2, 3.1, 3.8, 3.3):
    cells = []
    for method in (round, int, math.floor):
        rate, steps = rate_with(method, fat, 8.5)
        cells.append(f"{steps:>3} -> Rs {rate:6.2f}")
    print(f"   {fat:>5} {(fat - 3.5) / 0.1:>12.15g} | " + " | ".join(cells))
print("   fat 4.2 : all three methods agree here (the float error is +0.000000000000002, harmless for int/floor).")
print("   fat 3.1 : int() gives -3 steps (Rs 28.80), the correct rate is Rs 28.40 (-4 steps): int cuts towards zero.")
print("   fat 3.8 : int() and floor() both lose a step (2 instead of 3) because the float result is just below 3.")
print("   fat 3.3 : floor() gives -3 instead of -2 for the same reason on the negative side.")
print("   Only round() is correct for all four readings.")

n = 500000
for label, m in (("round", round), ("int", int), ("floor", math.floor)):
    t = timeit.timeit(lambda: m((4.2 - 3.5) / 0.1), number=n)
    print(f"   {label:<6} {n} evaluations: {t:.3f} s   (O(1) time, O(1) space)")
