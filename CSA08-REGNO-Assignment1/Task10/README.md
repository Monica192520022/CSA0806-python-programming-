# Task 10 - Compare Expectations with Execution (K4)

Run: `python task10_compare.py` (uses `calculator.py`, copied from Task 9)

Data: random but reproducible (seeded) entries; litres 2.00-35.00 L (2 decimals), fat 2.5-6.0, SNF 7.5-9.5. n = 300, 6,000, 150,000.

## What I expected
That float and Decimal totals would agree to within a few paise, and that rounding only the total would give the same result as rounding every payment.

## What happened (see the output)
| n | Reference A: Decimal, each payment rounded | B: Decimal, only the total rounded | C: float, each payment rounded |
|---|---|---|---|
| 300 | 178,428.00 | 178,427.81 (-0.19) | 178,427.88 (-0.12) |
| 6,000 | 3,658,301.01 | 3,658,298.34 (-2.67) | 3,658,298.46 (-2.55) |
| 150,000 | 91,718,915.26 | 91,718,852.09 (-63.17) | 91,718,851.78 (-63.48) |
(Yours will be identical because the data are seeded; only the times differ.)

1. **The totals do NOT agree.** The difference is not a few paise but grows with n: about Rs 0.19, Rs 2.67 and Rs 63 for 300, 6,000 and 150,000 payments.
2. **Reason:** the rate has one decimal (multiples of Rs 0.10) and the litres two, so `litres x rate` has 3 decimals and about **10 percent of payments end exactly in a half paisa** (for example 192.125). The bank rule rounds every payment half **up**, which adds +0.005 each time, so the sum of rounded payments is higher than the rounded sum of exact payments (expected bias +0.0005 per payment = about Rs 75 for 150,000). Rounding only the total (B, D) therefore does **not** reproduce the bank statement; every payment must be rounded first, then added. The rule of Task 1 (R6) is confirmed by evidence.
3. **float vs Decimal:** even with every payment rounded, float round() disagrees with the half-up rule for 12 / 255 / 6,348 payments (n = 300 / 6,000 / 150,000) - exact ties such as 192.125 are rounded to the nearest *even* paisa (192.12), and inexact binary values fall either way. Each such payment is one paisa wrong; the farmer is short-paid, and the union's total is wrong by Rs 63 at district scale. `Decimal` with `ROUND_HALF_UP` gives the bank amount.

## Timing (time.perf_counter, one run on my machine; yours will differ)
Decimal takes roughly 1.5-2x the time of float (for example 0.27 s vs 0.15 s for 150,000 entries), and the cost is linear: 20x more entries -> about 20x more time (O(n)). Both are fast enough: the whole district union's payment run takes well under a second for Decimal.

## Alternative concept and complexity analysis
**Rate table:** compute the rate of every (fat, snf) pair once, store it in a dictionary `{(fat, snf): rate}` and look it up for each entry.
* Time per entry: lookup is O(1) average (a hash of two Decimals); recalculation is also O(1) but with a large constant (two quantize operations, three multiplications). Measured over 150,000 entries the lookup version is about 5x faster in this program (0.04 s vs 0.25 s) and returns the same total.
* Space: the table holds k entries, O(k). Only 756 distinct pairs occurred in 150,000 entries; a complete table for all allowed readings (51 fat values x 31 SNF values = 1,581 pairs) is about 74 KB for the dictionary, built in about 2 ms. With 2-decimal analyser readings the number of pairs grows to 501 x 301 = 150,801, so the table may no longer be worth it - a lazy cache (fill on first use) would be better.
* Because the table is derived from the rate card, it must be rebuilt after every rate revision.

## Evidence
`output_task10_compare.txt` (below).

## Program output (as produced by my run)

### output_task10_compare.txt
```
1) Totals (A is the reference: Decimal, each payment rounded once to the paisa)
       n |   A Decimal each |   B Decimal once     B-A |     C float each (raw)          C-A |     D float once     D-A
     300 |        178428.00 |        178427.81   -0.19 |     178427.88000000006     -1.20E-1 |        178427.81   -0.19
           round(C,2) == A ? False
    6000 |       3658301.01 |       3658298.34   -2.67 |     3658298.4599999962     -2.55E+0 |       3658298.34   -2.67
           round(C,2) == A ? False
  150000 |      91718915.26 |      91718852.09  -63.17 |      91718851.77999999     -6.35E+1 |      91718852.09  -63.17
           round(C,2) == A ? False

2) How many single payments differ between float round() and Decimal ROUND_HALF_UP?
   n =    300: 12 payments differ by one paisa
   n =   6000: 255 payments differ by one paisa
   n = 150000: 6348 payments differ by one paisa

3) Time to compute (seconds, one run)
       n  Decimal each  Decimal once  float each  float once
     300        0.0006        0.0006      0.0003      0.0002
    6000        0.0106        0.0086      0.0071      0.0056
  150000        0.2815        0.2201      0.1574      0.1735

4) ALTERNATIVE: rate table (dictionary) instead of recalculating every entry
   distinct (fat, snf) pairs in 150,000 entries: k = 756
   full table (all 1581 allowed pairs) built in 0.0023 s, dict size 73808 bytes
   recalculate each entry : 0.2422 s  total 91718915.26
   dictionary lookup      : 0.0489 s  total 91718915.26
   same total? True   speed-up x4.95
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task10_run1.png`.
