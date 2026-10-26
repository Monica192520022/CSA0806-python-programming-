"""Task 9 - Ksheera Milk Co-operative payment calculator (final Decimal design).

Run:  python calculator.py               (interactive, one entry at a time)
      python calculator.py entries.csv   (batch: farmer_id,shift,litres,fat,snf)
"""
import csv
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# ---------------- named constants: the ONLY place where rates live ----------------
BASE_RATE = Decimal("30.00")        # Rs per litre at 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE = Decimal("0.40")    # Rs per litre for each 0.1 % of fat
SNF_STEP_VALUE = Decimal("0.30")    # Rs per litre for each 0.1 % of SNF
STD_FAT = Decimal("3.5")
STD_SNF = Decimal("8.5")
STEP = Decimal("0.1")
MIN_FAT, MAX_FAT = Decimal("2.0"), Decimal("7.0")
MIN_SNF, MAX_SNF = Decimal("7.0"), Decimal("10.0")   # assumption
MAX_LITRES = Decimal("500")                          # assumption
PAISA = Decimal("0.01")


def to_decimal(value, name):
    """Convert text/number to a finite Decimal or raise ValueError with a clear message."""
    text = str(value).strip()
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError(f"{name} '{text}' is not a valid number") from None
    if not number.is_finite():
        raise ValueError(f"{name} '{text}' is not a finite number")
    return number


def validate_entry(litres, fat, snf):
    """Return (litres, fat, snf) as Decimals, or raise ValueError if any rule is broken."""
    litres = to_decimal(litres, "litres")
    fat = to_decimal(fat, "fat")
    snf = to_decimal(snf, "snf")
    if not 0 < litres <= MAX_LITRES:
        raise ValueError(f"litres {litres} must be above 0 and at most {MAX_LITRES}")
    if not MIN_FAT <= fat <= MAX_FAT:
        raise ValueError(f"fat {fat} must be between {MIN_FAT} and {MAX_FAT}")
    if not MIN_SNF <= snf <= MAX_SNF:
        raise ValueError(f"snf {snf} must be between {MIN_SNF} and {MAX_SNF}")
    return litres, fat, snf


def count_steps(value, standard):
    """Number of whole 0.1 % steps of value from standard (nearest step, half up)."""
    return ((value - standard) / STEP).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def rate_per_litre(fat, snf):
    """Return the rate per litre as a Decimal with 2 decimals."""
    rate = (BASE_RATE + count_steps(fat, STD_FAT) * FAT_STEP_VALUE
            + count_steps(snf, STD_SNF) * SNF_STEP_VALUE)
    return rate.quantize(PAISA, rounding=ROUND_HALF_UP)


def payout(litres, fat, snf):
    """Return the amount payable for one entry, rounded ONCE to the paisa."""
    return (litres * rate_per_litre(fat, snf)).quantize(PAISA, rounding=ROUND_HALF_UP)


def ten_day_total(entries):
    """Return the sum of the already-rounded payouts of (litres, fat, snf) entries."""
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return total


def process_file(path):
    """Batch mode: print every entry, reject bad rows, print totals per farmer."""
    totals = {}
    print(f"{'Farmer':<8}{'Shift':<6}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>9}{'Amount':>11}")
    print("-" * 54)
    with open(path, newline="") as handle:
        for line_no, row in enumerate(csv.reader(handle), start=1):
            if not row:
                continue
            try:
                if len(row) != 5:
                    raise ValueError(f"expected 5 columns, found {len(row)}")
                farmer, shift = row[0].strip(), row[1].strip().upper()
                if shift not in ("M", "E"):
                    raise ValueError(f"shift '{shift}' must be M or E")
                litres, fat, snf = validate_entry(row[2], row[3], row[4])
            except ValueError as err:
                print(f"line {line_no}: REJECTED - {err}")
                continue
            rate, amount = rate_per_litre(fat, snf), payout(litres, fat, snf)
            totals[farmer] = totals.get(farmer, Decimal("0.00")) + amount
            print(f"{farmer:<8}{shift:<6}{litres:>8.2f}{fat:>6.1f}{snf:>6.1f}{rate:>9.2f}{amount:>11.2f}")
    print("-" * 54)
    for farmer, total in totals.items():
        print(f"Ten-day total {farmer}: Rs {total:,.2f}")
    print(f"Grand total      : Rs {sum(totals.values(), Decimal('0.00')):,.2f}")


def interactive():
    """Ask for one entry at a time until the farmer id is left empty."""
    total = Decimal("0.00")
    while True:
        farmer = input("Farmer id (blank to finish): ").strip()
        if not farmer:
            break
        try:
            litres, fat, snf = validate_entry(input("  litres: "), input("  fat %: "), input("  snf %: "))
        except ValueError as err:
            print("  REJECTED:", err)
            continue
        amount = payout(litres, fat, snf)
        total += amount
        print(f"  rate Rs {rate_per_litre(fat, snf):.2f}  amount Rs {amount:.2f}  running total Rs {total:,.2f}")
    print(f"Ten-day total: Rs {total:,.2f}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        interactive()
