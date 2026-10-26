# Task 11 - Recommend and Defend the Final Design (K5)

Files: `final_design.py` (Decimal design, rate card read from JSON), `rate_card.json`, `task11_recommend.py` (evidence)

Run: `python task11_recommend.py`

## Recommendation
| Decision | Recommendation | Evidence from my experiments |
|---|---|---|
| Type for money, litres, fat, SNF | `decimal.Decimal`, created from **text** (never from a float) | Task 2: float total `33400.30000000061` vs exact `33400.30`; `Decimal(float("33.40"))` is inexact. Task 10: float `round()` disagrees with the bank rule on 12 / 255 / 6,348 payments for n = 300 / 6,000 / 150,000 |
| Rounding rule | Round **each payment once** to the paisa with `ROUND_HALF_UP`, then add the rounded payments | Task 10: rounding only the total is Rs 0.19 / 2.67 / 63.17 away from the sum of payments for the three sizes (10 percent of payments are exact half-paisa ties) |
| Step counting | nearest whole 0.1 % step with `Decimal` (no float error) | Task 4: `(4.2-3.5)/0.1` and `int()`/`floor()` give wrong steps |
| Where the rates live | one rate card (named values, here a JSON file) read at start-up and validated | Task 3: magic numbers need k edits; one place needs one edit |
| Input handling | validate before use; reject, never guess | Task 5 and Task 9 tests I1-I11 |
| Testing | automated `assert` tests re-run after every rate revision | Task 9: 24 cases pass; Task 12: all cases pass |

## How a rate revision is carried out
1. Copy `rate_card.json` to a dated file (for example `rate_card_2026-04-01.json`) and edit the values; keep the old file so that past payments can be reproduced.
2. `load_rate_card()` refuses a missing, non-numeric, negative or zero-step value (section 3 of the output).
3. Run the test program with the new card, compare 3-5 hand-calculated payments (as in Task 9), then deploy the one file to every centre. **No Python code is edited** (section 2 of the output: the same entry pays 334.00 under the old card and 357.50 under the revised card).

## Limitations
* Decimal is slower than float (about 1.5-2x in Task 10), but this has no practical cost.
* The JSON file can still contain a wrong but valid number; validation cannot know the intended rate. Two persons should check each revision.
* Seasonal cards and the volume bonus are not in this design - Task 12 extends it.
* Entries are held in a list; for the union the data should be read row by row (a generator or `csv.reader`), which keeps memory O(1) (Task 8).
* The SNF range (7.0-10.0) and the 500 L limit are assumptions to be confirmed by the co-operative.

## Does it remain correct at district-union scale?
Yes. Decimal arithmetic is exact for any n, so correctness does not depend on size. In section 5 of the output, 150,000 entries are processed with the JSON rate card in well under a second; the time grows linearly (O(n)) and the extra memory is O(1) if the entries are streamed. The rounding rule matters **more** at scale: the half-up bias that is 19 paise at 300 payments is Rs 63 at 150,000.

## Alternative concept and complexity analysis
**Rate card in a JSON file, read when the program starts** (implemented), versus values written in the module (Task 7 / 9).
* Start-up time: reading t values is O(t) (the file is parsed once). Measured: 6 values (a real card) about 0.02 ms, 1,000 values about 0.05 ms, 100,000 values about 6 ms (see section 4 of the output, your times will differ). A real card has about 6 values, so the cost is negligible and paid once per run.
* Space: O(t) for the parsed values (6 `Decimal`s here); file size 139 bytes for 6 values.
* Maintenance: with values in the module every revision means editing source, re-testing and redistributing the **program** to every computer (c centres -> c copies of a code change, with the risk of syntax errors). With a JSON file only a small data file is changed and validated. Cost of the file approach: one more file that can be lost or edited wrongly, and a validation function that must be written (done in `load_rate_card`).

## Evidence
`output_task11_recommend.txt` (below).

## Program output (as produced by my run)

### output_task11_recommend.txt
```
1) Rate card loaded from rate_card.json
   RateCard(base_rate=Decimal('30.00'), fat_step_value=Decimal('0.40'), snf_step_value=Decimal('0.30'), std_fat=Decimal('3.5'), std_snf=Decimal('8.5'), step=Decimal('0.1'))
   rate for 4.2 / 8.7 = 33.40

2) A rate revision WITHOUT touching the program (new JSON file only)
   old card payout: 334.00   revised card payout: 357.50

3) The loader refuses a damaged rate card
   missing key  rejected -> rate card is missing 'base_rate'
   text value   rejected -> rate card value 'base_rate' = 'thirty' is not a number
   negative     rejected -> rate card value 'fat_step_value' must be a non-negative number
   zero step    rejected -> rate card 'step' must not be zero

4) ALTERNATIVE: start-up time and size to read t values from JSON
    t values  file bytes  read time (ms)
           6         139           0.032
        1000        6985           0.080
      100000      888973           6.082
   A real rate card has about 6 values: reading it costs a fraction of a millisecond, once.

5) Scale test with the final design (Decimal, JSON card)
   n =    300: total Rs     190,772.90   time 0.001 s
   n =   6000: total Rs   3,660,312.40   time 0.010 s
   n = 150000: total Rs  91,586,237.94   time 0.225 s

6) Limitations
   - Decimal is slower than float (roughly 1.5-2x in Task 10) - acceptable here: 150,000 entries take well under a second.
   - The JSON file can be edited wrongly; load_rate_card() validates but cannot know the intended rate.
   - Seasonal rates and the volume bonus need more than one card and a bonus rule (Task 12).
   - The whole list of entries is held in memory; a district union should read a file row by row.
   - SNF range (7.0-10.0) and MAX_LITRES (500) are assumptions that the union must confirm.
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task11_run1.png`.
