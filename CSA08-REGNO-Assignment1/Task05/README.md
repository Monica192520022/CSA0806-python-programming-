# Task 5 - Read Input and Convert Types (K3)

Run: `python task05_input.py` (uses simulated typing, so it runs without waiting for you). For real keyboard input: `python task05_input.py --interactive`

## input() returns a string
Even when the clerk types `8.5`, `input()` returns `'8.5'` (type `str`). Arithmetic needs conversion: `float('8.5')` or `int('3')` (the final calculator uses `Decimal`). `int('8.5')` raises `ValueError` because a whole number was requested.

## What happens with "8,5" or "eight"
`float("8,5")` and `float("eight")` raise `ValueError: could not convert string to float`. A program that does not check would crash in the middle of the clerk's work. A `while True` loop that asks again (`read_float`) with a clear message solves it (see section 3 of the output).

## Checking before converting (string methods)
`is_valid_number(text)`: strip spaces, allow one leading `-`, allow at most one `.`, and require the remaining characters to be decimal digits (`str.isdecimal()`, `str.count()`, `str.replace()`). `'8,5'`, `'eight'`, `''`, `'8.5.1'` are rejected; `' 8.5 '` is accepted after `strip()`.

## Formatted output with f-strings
`{name:<8}` left-aligned width 8, `{litres:>8.1f}` right-aligned, width 8, 1 decimal, `{amount:8.2f}` width 8, 2 decimals, `{value:^10.2f}` centred, `{total:,.2f}` thousands separator. The output shows a neat table.

## Alternative concept and complexity analysis
`parse_try(text)`: `try: float(text) except ValueError`.

| Input | String-method check | try/except |
|---|---|---|
| `"8,5"` | rejected | rejected (`ValueError`) |
| `" 8.5 "` | accepted (strip) | accepted - `float` ignores surrounding spaces |
| `"eight"` | rejected | rejected |
| `"1e2"` | rejected (`e` is not a digit) | **accepted** as 100.0 |
| `"nan"`, `"inf"` | rejected | **accepted by `float()`** - `nan` would pass every `<`/`>` comparison silently, so an extra `math.isfinite()` test is needed |

* Time per entry: both are O(L) in the length L of the text (a few characters), i.e. O(1) per entry. In the measurement the `try/except` version is faster for valid text (no extra scanning) but slower for invalid text, because raising and catching an exception is expensive. Clerks type valid values most of the time, so try/except is faster in practice.
* Clarity: `try/except` is shorter and accepts everything Python accepts (exponents, signs); the string method version is explicit about the format but easy to get wrong (it initially forgets `1e2` or Unicode digits).
* Space: O(1) in both.

## Evidence
`output_task05_input.txt` (below).

## Program output (as produced by my run)

### output_task05_input.txt
```
1) input() always returns a string
   typed 8.5 -> value = '8.5' type: str
   value + 1 would fail; float(value) + 1 = 9.5
   int('8.5') -> ValueError: invalid literal for int() with base 10: '8.5'

2) Checking input: string methods vs try/except
   text        str methods   try/except
   '8.5'              True          8.5
   '8,5'             False         None
   ' 8.5 '            True          8.5
   'eight'           False         None
   ''                False         None
   '-3'               True         -3.0
   '1e2'             False        100.0
   'nan'             False         None
   'inf'             False         None
   '8.5.1'           False         None
   '8.'               True          8.0
   '8,5' and 'eight' are rejected by both; ' 8.5 ' is accepted by both (spaces stripped).
   '1e2' is rejected by the str check but accepted by float(); 'nan'/'inf' need math.isfinite.

3) Retry loop with simulated typing: 8,5 -> eight -> 9.9 -> 4.2
Fat % (2.0-7.0): 8,5
   '8,5' is not a number. Use a dot, e.g. 8.5
Fat % (2.0-7.0): eight
   'eight' is not a number. Use a dot, e.g. 8.5
Fat % (2.0-7.0): 9.9
   9.9 is outside 2.0 .. 7.0
Fat % (2.0-7.0): 4.2
   accepted fat = 4.2

4) Aligned output with f-strings
   Farmer    Litres   Fat   SNF    Rate    Amount
   F001        10.0   3.5   8.5   30.00    300.00
   F002         8.5   4.2   8.7   33.40    283.90
   F003        12.0   3.1   8.3   27.80    333.60
   TOTAL                                   917.50
   centred: [   3.50   ]   zero padded: [00007.50]   thousands: [1,234,567.89]

5) ALTERNATIVE timing: valid and invalid text (200,000 repeats)
   input '8.5'    str methods: 0.033 s   try/except: 0.013 s
   input 'eight'  str methods: 0.028 s   try/except: 0.076 s
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task05_run1.png`.
