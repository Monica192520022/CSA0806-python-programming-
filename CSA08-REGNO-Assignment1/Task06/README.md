# Task 6 - Organise the Logic into Functions (K3)

Run: `python task06_functions.py`

## The functions
| Function | Parameters | Returns |
|---|---|---|
| `rate_per_litre(fat, snf)` | fat %, SNF % | rate in Rs per litre (2 decimals) |
| `payout(litres, fat, snf)` | quantity, fat, SNF | amount payable (2 decimals) |
| `ten_day_total(entries)` | list of `(litres, fat, snf)` | total of the payouts (2 decimals) |
Each function has a docstring (printed in the output as `f.__doc__`) and does one job; `payout` calls `rate_per_litre`, and `ten_day_total` calls `payout`.

## Return vs print
`return` hands the value back to the caller, who can store it, double it, add it or print it. `print` only shows text and the function returns `None` (the output shows `value stored from the print-only function: None`). Calculation functions should **return**; only the outer program prints.

## Local and global names
Constants such as `BASE_RATE` are global and can be **read** inside any function. Assigning `BASE_RATE = 99.0` inside a function creates a *new local* variable and leaves the global unchanged (the revision "applies only partly" - the original bug). `BASE_RATE += 1` inside a function raises `UnboundLocalError`, because Python decides the name is local. So: read constants in functions, change them only in the constants section (or the rate file).

## Alternative concept and complexity analysis
* **One long script, no functions:** the formula `round(l * round(30.0 + ..., 2), 2)` is pasted into every place where it is needed (a daily report, a ten-day report, a bank file). k places use the formula -> k copies to correct, and the repeated code length is proportional to k. Functions: the formula is written once.
* **`lambda`:** `rate_lambda = lambda fat, snf: ...` is a one-expression function without name/docstring support; suitable for short throw-away uses (`sorted(key=...)`), not for the main rules, because it cannot hold several statements and has no docstring.
* **Running time:** a function call adds a small constant cost per call. For n entries total time stays O(n) in all three styles; the measured table shows the no-function version about 10 percent faster, a difference that is irrelevant for 150,000 entries (about a tenth of a second) compared with the benefit of correctness and readability. Space is O(1) extra in all three.

## Evidence
`output_task06_functions.txt` (below).

## Program output (as produced by my run)

### output_task06_functions.txt
```
1) Return versus print
   returned value can be stored and reused: 283.9 -> doubled: 567.8
   printed: 283.9
   value stored from the print-only function: None

2) Local and global names
   BASE_RATE is read inside rate_per_litre without 'global' -> OK: 30.0
   bad_revision() returns 99.0 but global BASE_RATE is still 30.0
   UnboundLocalError: cannot access local variable 'BASE_RATE' where it is not associated with a value
   Rule: read constants inside functions, never change them there.

3) Docstrings
   rate_per_litre.__doc__ = Return the price per litre (float, 2 decimals) for the given fat % and SNF %.
   payout.__doc__ = Return the amount payable (float, 2 decimals) for one entry.
   ten_day_total.__doc__ = Return the total of all (litres, fat, snf) entries, rounded to 2 decimals.

4) The three entries of Task 7 through the functions
      10 L fat 3.5 snf 8.5 rate  30.00 pay   300.00
     8.5 L fat 4.2 snf 8.7 rate  33.40 pay   283.90
      12 L fat 3.1 snf 8.3 rate  27.80 pay   333.60
   ten_day_total = 917.5

5) ALTERNATIVE: no functions / lambda  (time for n entries, best of 3)
          n   functions  no functions    lambda   same total?
        300     0.00016       0.00015   0.00015   True
       6000     0.00328       0.00297   0.00322   True
     150000     0.08608       0.07600   0.08191   True
   Repeated code: functions = formula written once; no-function script = once per place used.
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task06_run1.png`.
