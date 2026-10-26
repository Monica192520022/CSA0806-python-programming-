# CSA08 - Assignment 1: Payment Calculator for the Ksheera Village Milk Co-operative

| | |
|---|---|
| Name | MONICA M|
| Register number | 192520022 |
| Course | CSA0806|
| Python version | Python 3.12 |
| Libraries | none - standard library only (see `requirements.txt`) |

## Repository layout
One folder per task. Each folder has the Python source, input files, the program output (`output_*.txt`), a `README.md` with the discussion, alternative concept and complexity analysis, and a `screenshots/` folder for your output screenshots.

## How to run everything
```
python run_all.py          # runs all programs and refreshes every output_*.txt
```
Or run each program separately:

| Task | Command (run inside the task folder) | Result |
|---|---|---|
| 1 Problem analysis | `python task01_analysis.py` | Data dictionary, constants, rules, assumptions; separate variables vs list measurement |
| 2 Values and types | `python task02_session.py`, `python task02_complete.py`, `python task02_alternatives.py` | `>>>` session; float total 33400.30000000061 vs Decimal 33400.30; paise / float / Decimal comparison |
| 3 Constants | `python task03_constants.py` | Naming, no true constants, dynamic typing, magic numbers vs constants vs dict |
| 4 Expressions | `python task04_expressions.py` | Precedence, float surprises, round/int/floor |
| 5 Input | `python task05_input.py` (`--interactive` for the keyboard) | String check vs try/except, f-string table |
| 6 Functions | `python task06_functions.py` | Functions, scope, no-function/lambda comparison |
| 7 Module | `python milkrate.py`, `python use_milkrate.py` | Expected table; `__name__` demo; import cost |
| 8 Algorithm | `python task08_algorithm.py` (+ `pseudocode.md`) | Hand trace = program; list vs running total |
| 9 Calculator | `python calculator.py entries.csv`, `python test_calculator.py` | Batch run; 24 tests, all pass |
| 10 Expectation vs execution | `python task10_compare.py` | float vs Decimal totals, timings, rate table |
| 11 Final design | `python task11_recommend.py` | JSON rate card, revision, scale test |
| 12 Design challenge | `python evaluate_old_design.py`, `python test_task12.py` | Impact of new requirements, seasons, bonus |

## Result summary
* Task 2: `float` gives 33400.30000000061, `Decimal` gives exactly 33400.30.
* Task 7: the module reproduces the expected table (300.00, 283.90, 333.60).
* Task 9: 24/24 tests pass; the 5-entry hand total 1593.23 matches.
* Task 10: rounding each payment to the paisa (half up) and then adding is the only method that matches the bank rule; float or "round only the total" are off by Rs 63 at 150,000 payments.
* Task 12: modified design (seasonal rate cards, proportional steps for 2-decimal readings, bonus function) passes all tests.

Timings in the output files depend on the computer; your own run will show different times but the same totals.
