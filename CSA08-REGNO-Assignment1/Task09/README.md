# Task 9 - Implement and Test the Calculator (K3)

Files: `calculator.py` (final calculator), `entries.csv` (input file with good and bad rows), `test_calculator.py` (assert-based tests with a printed test table)

Run:
```
python calculator.py entries.csv     # batch mode -> output_calculator.txt
python calculator.py                 # interactive mode: type one entry at a time
python test_calculator.py            # 24 test cases
```

## Design
* All money, litres, fat and SNF are `decimal.Decimal`, built from the typed **text** - never from a float.
* All rates and limits are named constants at the top of the file.
* `validate_entry()` enforces the rules of Task 1 and raises `ValueError` with a clear message (text, negative, out of range, `8,5`, `nan`).
* `count_steps()` rounds to the nearest 0.1 % step with `ROUND_HALF_UP`; `payout()` rounds **once** to the paisa; `ten_day_total()` adds the rounded payouts.

## Test table (also printed by the test program)
| Group | Cases | Result |
|---|---|---|
| Normal, each direction (fat above/below, SNF above/below, both) | N1-N7 | all pass |
| Boundary: exactly 3.5 % / 8.5 %; lowest and highest fat (2.0, 7.0); lowest and highest SNF (7.0, 10.0); half-paisa rounding (192.125 -> 192.13) | N1, B1-B5 | all pass |
| Invalid: text, negative, zero, too large, fat outside range, `'eight'`, `'8,5'`, SNF outside range, `nan`, empty | I1-I11 | all rejected with `ValueError` |
| Five entries with a total calculated by hand | H1 | 300.00 + 283.90 + 333.60 + 483.60 + 192.13 = **1593.23**, program = 1593.23 |
The complete table with expected and actual values is in `output_test_calculator.txt` below.

The batch run of `entries.csv` shows 6 accepted entries (F001 total Rs 1,593.23, F002 Rs 646.00, grand total Rs 2,239.23) and 4 rejected lines (text litres, fat 7.5, negative litres, and a malformed row with 6 columns), each with its reason.

## Alternative concept and complexity analysis
**Manual testing:** typing every case by hand each time, reading the screen and judging it by eye.
**Automated testing:** a function with `assert` statements (`test_calculator.py`) that runs all cases in one command.

| | Manual | `assert` tests |
|---|---|---|
| Time to rerun all m tests after one change | O(m) **human** actions - typing 3 values per case, several minutes for 24 cases | O(m) **machine** operations - well under a second; one command |
| Reliability | easy to forget a case or misread a number | every case checked every time; a failure stops with the case ID |
| Cost of a new change | grows with m x number of changes | almost zero after the tests are written |
Both are O(m) in the number of test cases, but the constant for the human is minutes and for the computer is microseconds, so automated tests are re-run after every change (rate revision, new rule) at no cost.

## Evidence
`output_calculator.txt`, `output_test_calculator.txt` (below). Take screenshots of both runs for the report.

## Program output (as produced by my run)

### output_calculator.txt
```
Farmer  Shift   Litres   Fat   SNF     Rate     Amount
------------------------------------------------------
F001    M        10.00   3.5   8.5    30.00     300.00
F001    E         8.50   4.2   8.7    33.40     283.90
F001    M        12.00   3.1   8.3    27.80     333.60
F001    E        15.50   3.8   8.5    31.20     483.60
F001    M         7.25   3.0   8.0    26.50     192.13
line 6: REJECTED - litres 'abc' is not a valid number
line 7: REJECTED - fat 7.5 must be between 2.0 and 7.0
F002    M        20.00   4.0   8.6    32.30     646.00
line 9: REJECTED - litres -5 must be above 0 and at most 500
line 10: REJECTED - expected 5 columns, found 6
------------------------------------------------------
Ten-day total F001: Rs 1,593.23
Ten-day total F002: Rs 646.00
Grand total      : Rs 2,239.23
```

### output_test_calculator.txt
```
ID  Case                        Input (L, fat, snf)     Expected            Actual              Result
----------------------------------------------------------------------------------------------------------
N1  standard milk               10, 3.5, 8.5            30.00 / 300.00      30.00 / 300.00      PASS
N2  fat above standard          8.5, 4.2, 8.5           32.80 / 278.80      32.80 / 278.80      PASS
N3  fat below standard          10, 3.1, 8.5            28.40 / 284.00      28.40 / 284.00      PASS
N4  SNF above standard          10, 3.5, 8.9            31.20 / 312.00      31.20 / 312.00      PASS
N5  SNF below standard          10, 3.5, 8.1            28.80 / 288.00      28.80 / 288.00      PASS
N6  fat and SNF above           8.5, 4.2, 8.7           33.40 / 283.90      33.40 / 283.90      PASS
N7  fat and SNF below           12, 3.1, 8.3            27.80 / 333.60      27.80 / 333.60      PASS
B1  boundary: lowest fat 2.0    10, 2.0, 8.5            24.00 / 240.00      24.00 / 240.00      PASS
B2  boundary: highest fat 7.0   10, 7.0, 8.5            44.00 / 440.00      44.00 / 440.00      PASS
B3  boundary: lowest SNF 7.0    10, 3.5, 7.0            25.50 / 255.00      25.50 / 255.00      PASS
B4  boundary: highest SNF 10.0  10, 3.5, 10.0           34.50 / 345.00      34.50 / 345.00      PASS
B5  half-paisa rounds up        7.25, 3.0, 8.0          26.50 / 192.13      26.50 / 192.13      PASS
I1  text instead of litres      abc, 3.5, 8.5           ValueError          ValueError          PASS
I2  negative litres             -5, 3.5, 8.5            ValueError          ValueError          PASS
I3  zero litres                 0, 3.5, 8.5             ValueError          ValueError          PASS
I4  litres too large            501, 3.5, 8.5           ValueError          ValueError          PASS
I5  fat below 2.0               10, 1.9, 8.5            ValueError          ValueError          PASS
I6  fat above 7.0               10, 7.1, 8.5            ValueError          ValueError          PASS
I7  fat typed as 'eight'        10, eight, 8.5          ValueError          ValueError          PASS
I8  comma decimal '8,5'         10, 3.5, 8,5            ValueError          ValueError          PASS
I9  SNF below 7.0               10, 3.5, 6.9            ValueError          ValueError          PASS
I10 nan as fat                  10, nan, 8.5            ValueError          ValueError          PASS
I11 empty litres                <empty>, 3.5, 8.5       ValueError          ValueError          PASS
H1  5 entries, total by hand    5 entries               1593.23             1593.23             PASS
----------------------------------------------------------------------------------------------------------
24 test cases, 0 failures
All tests passed.
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task09_run1.png`.
