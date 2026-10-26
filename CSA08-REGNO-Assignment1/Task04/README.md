# Task 4 - Write Correct Expressions (K4)

Run: `python task04_expressions.py`

## The expressions
```python
fat_steps = round((fat - 3.5) / 0.1)
snf_steps = round((snf - 8.5) / 0.1)
rate      = round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)
amount    = round(litres * rate, 2)
valid     = litres > 0 and 2.0 <= fat <= 7.0
```
(The final program in Task 9 uses `Decimal`; here `float` is used to show the problems.)

## Precedence and associativity (from the output)
* `**` binds tighter than unary minus: `-2 ** 2` = `-4`, but `(-2) ** 2` = `4`.
* `**` is right-associative: `2 ** 3 ** 2` = `2 ** 9` = `512`; `(2 ** 3) ** 2` = `64`.
* `*` before `+`: `2 + 3 * 4` = 14. `-` is left-associative: `10 - 4 - 3` = 3.
* `not` > `and` > `or`: `True or False and False` is `True`.
* Comparison chaining: `2.0 <= fat <= 7.0` means `2.0 <= fat and fat <= 7.0`; `1 < 2 < 3 > 2` is `True`. `and`/`or` short-circuit: `False and (1/0)` never evaluates `1/0`.

## Surprising results
1. `(4.2 - 3.5) / 0.1` is **not 7** (it prints `7.000000000000002` on my machine; the assignment quotes `7.000000000000001` - the exact last digits depend on the subtraction, the point is the same): 4.2, 3.5 and 0.1 cannot be stored exactly in binary. `round(...)` returns the intended step count 7.
2. `(3.8 - 3.5) / 0.1` is `2.9999999999999982`, so `int()` gives **2** instead of 3 - a wrong step count (a wrong payment).
3. `round(2.5)` is `2` and `round(3.5)` is `4`: Python rounds exact halves to the nearest **even** number. (This matters again for money in Task 10.)
4. `0.1 * 3` -> `0.30000000000000004`, `1.1 + 2.2` -> `3.3000000000000003`, `-2 ** 2` -> `-4`.

## round() vs int() vs math.floor() for negative values
| x | round | int | floor |
|---|---|---|---|
| -2.5 | -2 | -2 | -3 |
| -0.6 | -1 | 0 | -1 |
| -0.4 | 0 | 0 | -1 |
| 2.6 | 3 | 2 | 2 |
`int()` truncates toward zero, `floor()` goes toward minus infinity, `round()` goes to the nearest integer. For a fat value **below** the standard (negative steps) they give different results.

## Alternative concept and complexity analysis
Number of steps computed with `int()` or `math.floor()` instead of `round()` (snf = 8.5):

| fat | exact steps | round -> rate | int -> rate | floor -> rate |
|---|---|---|---|---|
| 4.2 | 7 | 7 -> Rs 32.80 | 7 -> Rs 32.80 | 7 -> Rs 32.80 |
| 3.1 | -4 | -4 -> **Rs 28.40** | -3 -> Rs 28.80 (wrong) | -4 -> Rs 28.40 |
| 3.8 | 3 | 3 -> **Rs 31.20** | 2 -> Rs 30.80 (wrong) | 2 -> Rs 30.80 (wrong) |
| 3.3 | -2 | -2 -> **Rs 29.20** | -2 -> Rs 29.20 | -3 -> Rs 28.80 (wrong) |

For fat = 4.2 all three agree here only because the float error happens to be positive (+2e-15). For fat = 3.1 `int()` is wrong because it truncates `-3.999...` toward zero. `floor()` fails whenever the float result falls just below an integer. `round()` is correct for all because it absorbs errors up to half a step. Time and space of each method: one call and one result - **O(1) time, O(1) space**; the timings in the output differ by microseconds, so correctness decides, not speed.

## Evidence
`output_task04_expressions.txt` (below).

## Program output (as produced by my run)

### output_task04_expressions.txt
```
1) Operator precedence and associativity
   2 + 3 * 4                  = 14
   (2 + 3) * 4                = 20
   -2 ** 2                    = -4
   (-2) ** 2                  = 4
   2 ** 3 ** 2                = 512
   (2 ** 3) ** 2              = 64
   10 - 4 - 3                 = 3
   -7 // 2                    = -4
   not True or True           = True
   True or False and False    = True

2) Surprising results (floating point and rounding)
   (4.2 - 3.5) / 0.1            -> 7.000000000000002
   (3.8 - 3.5) / 0.1            -> 2.9999999999999982
   int((3.8 - 3.5) / 0.1)       -> 2
   round((3.8 - 3.5) / 0.1)     -> 3
   0.1 * 3                      -> 0.30000000000000004
   1.1 + 2.2                    -> 3.3000000000000003
   round(2.5), round(3.5)       -> (2, 4)
   -2 ** 2                      -> -4
   (4.2-3.5)/0.1 is 7.000000000000002, not 7 (the assignment quotes 7.000000000000001; the last
   digits depend on the exact subtraction), because 4.2, 3.5 and 0.1 cannot all be
   stored exactly in binary; round() brings the step count back to 7.
   (3.8-3.5)/0.1 is 2.9999999999999982: int() truncates it to 2 -> a WRONG step count.
   round(2.5)=2 and round(3.5)=4: Python rounds exact halves to the even number.

3) round(), int() and math.floor() for negative values
        x  round   int  floor
     -2.5     -2    -2     -3
     -2.4     -2    -2     -3
     -0.6     -1     0     -1
     -0.4      0     0     -1
      0.4      0     0      0
      2.6      3     2      2
   int() cuts towards zero, floor() goes down, round() goes to the nearest.

4) Comparison chaining and Boolean operators
   2.0 <= fat <= 7.0 with fat=4.2 : True
   2.0 <= 7.5 <= 7.0              : False
   1 < 2 < 3 > 2                  : True
   litres > 0 and 7.0 <= snf <= 10.0 : True
   short circuit: False and (1/0)  : False

5) The final expression (round-based steps) for the three entries of Task 7
   fat 3.5 snf 8.5: fat_steps =   0, rate = 30.00
   fat 4.2 snf 8.7: fat_steps =   7, rate = 33.40
   fat 3.1 snf 8.3: fat_steps =  -4, rate = 27.80

6) ALTERNATIVE: int() / math.floor() instead of round()  (snf = 8.5)
     fat  exact steps |          round |            int |          floor
     4.2            7 |   7 -> Rs  32.80 |   7 -> Rs  32.80 |   7 -> Rs  32.80
     3.1           -4 |  -4 -> Rs  28.40 |  -3 -> Rs  28.80 |  -4 -> Rs  28.40
     3.8            3 |   3 -> Rs  31.20 |   2 -> Rs  30.80 |   2 -> Rs  30.80
     3.3           -2 |  -2 -> Rs  29.20 |  -2 -> Rs  29.20 |  -3 -> Rs  28.80
   fat 4.2 : all three methods agree here (the float error is +0.000000000000002, harmless for int/floor).
   fat 3.1 : int() gives -3 steps (Rs 28.80), the correct rate is Rs 28.40 (-4 steps): int cuts towards zero.
   fat 3.8 : int() and floor() both lose a step (2 instead of 3) because the float result is just below 3.
   fat 3.3 : floor() gives -3 instead of -2 for the same reason on the negative side.
   Only round() is correct for all four readings.
   round  500000 evaluations: 0.023 s   (O(1) time, O(1) space)
   int    500000 evaluations: 0.019 s   (O(1) time, O(1) space)
   floor  500000 evaluations: 0.011 s   (O(1) time, O(1) space)
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task04_run1.png`.
