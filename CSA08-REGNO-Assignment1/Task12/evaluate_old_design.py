"""Task 12 B - evaluates the ORIGINAL design (Task 7 module) against the new requirements."""
from decimal import Decimal as D, ROUND_HALF_UP

import milkrate_v1 as old
import milkrate_v2 as new

print("1) Two-decimal readings: old design vs new design (standard season, 10 litres)")
print(f"   {'fat':>5} {'snf':>5} | {'old rate':>9} {'old pay':>9} | {'new rate':>9} {'new pay':>9} | {'old-new':>8}")
for fat, snf in (("3.50", "8.50"), ("3.54", "8.54"), ("3.57", "8.53"), ("3.64", "8.46"), ("4.23", "8.68")):
    o_rate, o_pay = old.rate_per_litre(float(fat), float(snf)), old.payout(10, float(fat), float(snf))
    n_rate = new.rate_per_litre(D(fat), D(snf))
    n_pay = new.payout(D("10"), D(fat), D(snf))
    print(f"   {fat:>5} {snf:>5} | {o_rate:>9.2f} {o_pay:>9.2f} | {n_rate:>9} {n_pay:>9} | {D(str(o_pay)) - n_pay:>8}")
print("   The old module rounds 3.57 % to the 3.6 % step, so the farmer is overpaid or underpaid.")

print("\n2) Tie readings (x.x5): float step counting vs exact Decimal step counting")
mismatch = 0
examples = []
for hundredths in range(200, 701):
    fat_text = f"{hundredths / 100:.2f}"
    old_steps = round((float(fat_text) - 3.5) / 0.1)
    new_steps = new.count_steps(D(fat_text), new.STD_FAT, "nearest")
    if old_steps != new_steps:
        mismatch += 1
        if len(examples) < 4:
            examples.append((fat_text, (float(fat_text) - 3.5) / 0.1, old_steps, new_steps))
print(f"   fat readings 2.00 .. 7.00 where float and Decimal disagree on the step: {mismatch} of 501")
for fat_text, raw, o, n in examples:
    print(f"   fat {fat_text}: float steps = {raw!r} -> round gives {o}, Decimal gives {n}")

print("\n3) What the old module cannot express")
print("   - It has ONE BASE_RATE = 30.00 and ONE FAT_STEP_VALUE = 0.40 (module-level names).")
print("   - Summer rates need base 32.00 and fat step 0.45: the module would have to be edited,")
print("     or the constants changed at run time (global state - dangerous).")
print("   - No function knows about ten-day litres, so the Rs 0.50 bonus has no place to live.")
print(f"   old payout for summer entry 10 L, 3.5 / 8.5 = {old.payout(10, 3.5, 8.5)} (should be 320.00)")
