"""Task 3 - Variables and named constants."""
import inspect
import keyword
import timeit
from types import MappingProxyType
from typing import Final

# ---------------- the single place where rates live ----------------
BASE_RATE: Final = 30.00        # Rs per litre at 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE: Final = 0.40    # Rs per litre per 0.1 % fat from standard
SNF_STEP_VALUE: Final = 0.30    # Rs per litre per 0.1 % SNF from standard
STD_FAT: Final = 3.5
STD_SNF: Final = 8.5
STEP: Final = 0.1
MIN_FAT: Final = 2.0
MAX_FAT: Final = 7.0


def rate_per_litre(fat, snf):
    fat_steps = round((fat - STD_FAT) / STEP)
    snf_steps = round((snf - STD_SNF) / STEP)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


print("1) Naming rules")
for name in ("fat", "fat_percent", "FAT_STEP_VALUE", "2fat", "fat-percent", "class", "_total"):
    ok = name.isidentifier() and not keyword.iskeyword(name)
    print(f"   {name!r:18} valid identifier? {ok}")
print("   Convention: snake_case for variables/functions, UPPER_CASE for constants.")

print("\n2) Python has no true constants")
print("   BASE_RATE before:", BASE_RATE)
BASE_RATE = 99.0          # Python allows this silently; Final only helps type checkers
print("   BASE_RATE after re-assignment:", BASE_RATE, "(no error!)")
BASE_RATE = 30.00         # restore
card = MappingProxyType({"base": 30.0, "fat": 0.40, "snf": 0.30})
try:
    card["base"] = 99.0
except TypeError as err:
    print("   read-only mapping (MappingProxyType) refuses change ->", err)

print("\n3) Dynamic typing")
x = 8
print("   x =", x, "->", type(x).__name__)
x = "eight"
print("   x =", x, "->", type(x).__name__, "(same name, new type, no error)")
try:
    litres = 10
    print(litres + "5")
except TypeError as err:
    print("   TypeError only when the operation is executed ->", err)

print("\n4) Multiple assignment and swapping")
fat, snf = 3.5, 8.5
print("   before:", fat, snf)
fat, snf = snf, fat
print("   after a, b = b, a :", fat, snf)
a = b = 0
print("   a = b = 0 ->", a, b)


# ---------------- alternative concepts ----------------
def rate_magic_1(fat, snf):
    return round(30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)


def rate_magic_2(fat, snf):          # a second report that repeats the rates
    return 30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30


def rate_magic_3(fat, snf):          # a third place (e.g. bank file generator)
    base, fat_value, snf_value = 30.0, 0.40, 0.30
    return base + round((fat - 3.5) / 0.1) * fat_value + round((snf - 8.5) / 0.1) * snf_value


RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}


def rate_dict(fat, snf):
    return round(RATE_CARD["base"] + round((fat - 3.5) / 0.1) * RATE_CARD["fat"]
                 + round((snf - 8.5) / 0.1) * RATE_CARD["snf"], 2)


print("\n5) Alternative: magic numbers vs constants vs dictionary")
source = "".join(inspect.getsource(f) for f in (rate_magic_1, rate_magic_2, rate_magic_3))
print("   places holding the number 0.40 in the magic-number design:", source.count("0.40"))
print("   places holding the number 0.40 in the constants design   : 1 (FAT_STEP_VALUE)")
print("   places holding the number 0.40 in the dictionary design  : 1 (RATE_CARD['fat'])")
print("   results equal for (4.2, 8.7):", rate_per_litre(4.2, 8.7), rate_magic_1(4.2, 8.7), rate_dict(4.2, 8.7))

n = 300000
for label, fn in (("constants", rate_per_litre), ("magic numbers", rate_magic_1), ("dictionary", rate_dict)):
    t = timeit.timeit(lambda: fn(4.2, 8.7), number=n)
    print(f"   {label:<14} {n} calls: {t:.3f} s")
print("   Memory: constants = 3 names, dictionary = 1 dict object; both O(1).")
