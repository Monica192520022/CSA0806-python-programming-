"""Task 11 - Final design: Decimal arithmetic, rate card read from a JSON file."""
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

PAISA = Decimal("0.01")
REQUIRED = ("base_rate", "fat_step_value", "snf_step_value", "std_fat", "std_snf", "step")


@dataclass(frozen=True)
class RateCard:
    base_rate: Decimal
    fat_step_value: Decimal
    snf_step_value: Decimal
    std_fat: Decimal
    std_snf: Decimal
    step: Decimal


def load_rate_card(path):
    """Read and validate a rate card; raise ValueError for a missing/bad value."""
    with open(path) as handle:
        raw = json.load(handle)
    values = {}
    for key in REQUIRED:
        if key not in raw:
            raise ValueError(f"rate card is missing '{key}'")
        try:
            values[key] = Decimal(str(raw[key]))
        except InvalidOperation:
            raise ValueError(f"rate card value '{key}' = {raw[key]!r} is not a number") from None
        if not values[key].is_finite() or values[key] < 0:
            raise ValueError(f"rate card value '{key}' must be a non-negative number")
    if values["step"] == 0:
        raise ValueError("rate card 'step' must not be zero")
    return RateCard(**values)


def count_steps(value, standard, step):
    return ((value - standard) / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def rate_per_litre(card, fat, snf):
    rate = (card.base_rate + count_steps(fat, card.std_fat, card.step) * card.fat_step_value
            + count_steps(snf, card.std_snf, card.step) * card.snf_step_value)
    return rate.quantize(PAISA, rounding=ROUND_HALF_UP)


def payout(card, litres, fat, snf):
    return (litres * rate_per_litre(card, fat, snf)).quantize(PAISA, rounding=ROUND_HALF_UP)


def ten_day_total(card, entries):
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += payout(card, litres, fat, snf)
    return total
