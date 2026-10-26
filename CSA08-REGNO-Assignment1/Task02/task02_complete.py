"""Task 2 - Complete the Code (TODO 1 done)."""
from decimal import Decimal

# 1,000 payments of Rs 33.40 and three small adjustments of Rs 0.10
payments = ["33.40"] * 1000 + ["0.10"] * 3


def total_float(items):
    total = 0.0
    for amount in items:
        total += float(amount)
    return total


def total_decimal(items):
    # TODO 1 (done): add the amounts exactly by creating a Decimal from each string
    total = Decimal("0")
    for amount in items:
        total += Decimal(amount)
    return total


def total_decimal_from_float(items):
    """The 'wrong' variant asked in the task: Decimal(float(amount))."""
    total = Decimal("0")
    for amount in items:
        total += Decimal(float(amount))
    return total


print("float  :", total_float(payments))
print("Decimal:", total_decimal(payments))
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

print("\n--- Change asked in the task: Decimal(float(amount)) ---")
wrong = total_decimal_from_float(payments)
print("Decimal(float(amount)) total :", wrong)
print("Equals 33400.30 ?            :", wrong == Decimal("33400.30"))
print("Decimal(float('33.40'))      :", Decimal(float("33.40")))
