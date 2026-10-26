"""Task 11 - Evidence for the recommended design and the JSON rate-card alternative."""
import json
import os
import random
import sys
import tempfile
import time
from decimal import Decimal

from final_design import RateCard, load_rate_card, payout, rate_per_litre, ten_day_total

HERE = os.path.dirname(os.path.abspath(__file__))
card = load_rate_card(os.path.join(HERE, "rate_card.json"))

print("1) Rate card loaded from rate_card.json")
print("  ", card)
print("   rate for 4.2 / 8.7 =", rate_per_litre(card, Decimal("4.2"), Decimal("8.7")))

print("\n2) A rate revision WITHOUT touching the program (new JSON file only)")
folder = tempfile.mkdtemp()
revised_path = os.path.join(folder, "rate_card_revised.json")
revised = {"base_rate": "32.00", "fat_step_value": "0.45", "snf_step_value": "0.30",
           "std_fat": "3.5", "std_snf": "8.5", "step": "0.1"}
with open(revised_path, "w") as f:
    json.dump(revised, f)
new_card = load_rate_card(revised_path)
entry = (Decimal("10"), Decimal("4.2"), Decimal("8.7"))
print("   old card payout:", payout(card, *entry), "  revised card payout:", payout(new_card, *entry))

print("\n3) The loader refuses a damaged rate card")
for label, change in (("missing key", lambda d: d.pop("base_rate")),
                      ("text value", lambda d: d.update(base_rate="thirty")),
                      ("negative", lambda d: d.update(fat_step_value="-0.4")),
                      ("zero step", lambda d: d.update(step="0"))):
    data = dict(revised)
    change(data)
    path = os.path.join(folder, "bad.json")
    with open(path, "w") as f:
        json.dump(data, f)
    try:
        load_rate_card(path)
        print(f"   {label:<12} accepted (BAD)")
    except ValueError as err:
        print(f"   {label:<12} rejected -> {err}")

print("\n4) ALTERNATIVE: start-up time and size to read t values from JSON")
print(f"   {'t values':>9} {'file bytes':>11} {'read time (ms)':>15}")
for t in (6, 1000, 100000):
    data = dict(revised)
    data["extras"] = [str(i) for i in range(t - 6)] if t > 6 else []
    path = os.path.join(folder, f"t{t}.json")
    with open(path, "w") as f:
        json.dump(data, f)
    t0 = time.perf_counter()
    with open(path) as f:
        json.load(f)
    ms = (time.perf_counter() - t0) * 1000
    print(f"   {t:>9} {os.path.getsize(path):>11} {ms:>15.3f}")
print("   A real rate card has about 6 values: reading it costs a fraction of a millisecond, once.")

print("\n5) Scale test with the final design (Decimal, JSON card)")
rng = random.Random(1)
for n in (300, 6000, 150000):
    entries = [(Decimal(rng.randint(200, 3500)) / 100, Decimal(rng.randint(25, 60)) / 10,
                Decimal(rng.randint(75, 95)) / 10) for _ in range(n)]
    t0 = time.perf_counter()
    total = ten_day_total(card, entries)
    print(f"   n = {n:>6}: total Rs {total:>14,.2f}   time {time.perf_counter() - t0:.3f} s")

print("\n6) Limitations")
for text in ("Decimal is slower than float (roughly 1.5-2x in Task 10) - acceptable here: 150,000 entries take well under a second.",
             "The JSON file can be edited wrongly; load_rate_card() validates but cannot know the intended rate.",
             "Seasonal rates and the volume bonus need more than one card and a bonus rule (Task 12).",
             "The whole list of entries is held in memory; a district union should read a file row by row.",
             "SNF range (7.0-10.0) and MAX_LITRES (500) are assumptions that the union must confirm."):
    print("   -", text)
