"""Task 12 - Redesigned rate module: seasons, two-decimal readings, volume bonus.

Design decisions
  * RATE_CARDS holds one RateCard per season; the season is a PARAMETER.
  * season_for_month() picks the card (April-June = "summer").
  * Readings arrive with 2 decimals, so steps are counted PROPORTIONALLY
    (3.57 % fat = 0.7 step) instead of being rounded to a whole 0.1 % step.
    mode="nearest" keeps the old behaviour for comparison.
  * The bonus is a separate function applied to the ten-day litres.
"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

D = Decimal
PAISA = D("0.01")
STEP = D("0.1")
STD_FAT, STD_SNF = D("3.5"), D("8.5")
MIN_FAT, MAX_FAT = D("2.0"), D("7.0")
MIN_SNF, MAX_SNF = D("7.0"), D("10.0")
MAX_LITRES = D("500")
SUMMER_MONTHS = (4, 5, 6)
BONUS_THRESHOLD_LITRES = D("500")     # bonus only if MORE than this in ten days
BONUS_PER_LITRE = D("0.50")


@dataclass(frozen=True)
class RateCard:
    name: str
    base_rate: Decimal
    fat_step_value: Decimal
    snf_step_value: Decimal


RATE_CARDS = {
    "standard": RateCard("standard", D("30.00"), D("0.40"), D("0.30")),
    "summer": RateCard("summer", D("32.00"), D("0.45"), D("0.30")),
}


def season_for_month(month):
    """Return 'summer' for April-June (4-6) and 'standard' otherwise."""
    if not isinstance(month, int) or not 1 <= month <= 12:
        raise ValueError(f"month {month!r} must be a whole number from 1 to 12")
    return "summer" if month in SUMMER_MONTHS else "standard"


def to_decimal(value, name, max_places=2):
    """Convert to a finite Decimal with at most max_places decimals (analyser gives 2)."""
    text = str(value).strip()
    try:
        number = D(text)
    except InvalidOperation:
        raise ValueError(f"{name} '{text}' is not a valid number") from None
    if not number.is_finite():
        raise ValueError(f"{name} '{text}' is not a finite number")
    if number.as_tuple().exponent < -max_places:
        raise ValueError(f"{name} '{text}' has more than {max_places} decimals")
    return number


def validate_entry(litres, fat, snf):
    """Return (litres, fat, snf) as Decimals or raise ValueError."""
    litres, fat, snf = to_decimal(litres, "litres"), to_decimal(fat, "fat"), to_decimal(snf, "snf")
    if not 0 < litres <= MAX_LITRES:
        raise ValueError(f"litres {litres} must be above 0 and at most {MAX_LITRES}")
    if not MIN_FAT <= fat <= MAX_FAT:
        raise ValueError(f"fat {fat} must be between {MIN_FAT} and {MAX_FAT}")
    if not MIN_SNF <= snf <= MAX_SNF:
        raise ValueError(f"snf {snf} must be between {MIN_SNF} and {MAX_SNF}")
    return litres, fat, snf


def count_steps(value, standard, mode="proportional"):
    """Steps of 0.1 % from standard: exact fraction, or nearest whole step."""
    steps = (value - standard) / STEP
    if mode == "nearest":
        return steps.quantize(D("1"), rounding=ROUND_HALF_UP)
    if mode == "proportional":
        return steps
    raise ValueError("mode must be 'proportional' or 'nearest'")


def rate_per_litre(fat, snf, season="standard", mode="proportional"):
    """Rate per litre (2 decimals, half up) for the season's rate card."""
    card = RATE_CARDS[season]
    rate = (card.base_rate + count_steps(fat, STD_FAT, mode) * card.fat_step_value
            + count_steps(snf, STD_SNF, mode) * card.snf_step_value)
    return rate.quantize(PAISA, rounding=ROUND_HALF_UP)


def payout(litres, fat, snf, season="standard", mode="proportional"):
    """Amount for one entry, rounded once to the paisa."""
    return (litres * rate_per_litre(fat, snf, season, mode)).quantize(PAISA, rounding=ROUND_HALF_UP)


def bonus(total_litres):
    """Rs 0.50 per litre on ALL litres when the ten-day supply is MORE than 500 L."""
    if total_litres > BONUS_THRESHOLD_LITRES:
        return (total_litres * BONUS_PER_LITRE).quantize(PAISA, rounding=ROUND_HALF_UP)
    return D("0.00")


def ten_day_summary(entries, season="standard", mode="proportional"):
    """Return dict(litres, base_amount, bonus, total) for (litres, fat, snf) entries."""
    litres_total = D("0")
    base = D("0.00")
    for litres, fat, snf in entries:
        litres_total += litres
        base += payout(litres, fat, snf, season, mode)
    extra = bonus(litres_total)
    return {"litres": litres_total, "base_amount": base, "bonus": extra, "total": base + extra}
