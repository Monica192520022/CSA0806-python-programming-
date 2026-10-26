# Task 2 - Explore Values and Types in the Interpreter (K4)

Run:
* `python task02_session.py` - reproduces an interactive `>>>` session (paste this as evidence; also run `python` yourself and take a screenshot of the real prompt)
* `python task02_complete.py` - Complete the Code (TODO 1 done) + the `Decimal(float(amount))` experiment
* `python task02_alternatives.py` - integer paise vs float+round vs Decimal

## Types (from the session)
`type(10)` -> `int`; `type(10.0)` -> `float`; `type("10")` -> `str`; `type(True)` -> `bool`; `type([10, 8.5])` -> `list`.
Surprise: `isinstance(True, int)` is `True` and `True + True` is `2` - `bool` is a subclass of `int`.

## Division operators
| Expression | Result | Explanation |
|---|---|---|
| `7 / 2` | `3.5` | `/` is true division, always a `float`. |
| `7 // 2` | `3` | `//` is floor division. |
| `7 % 2` | `1` | remainder. |
| `-7 // 2` | `-4` | **surprise:** floor division rounds toward minus infinity, not toward zero. |
| `-7 % 2` | `1` | keeps the identity `(a // b) * b + a % b == a`: `(-4)*2 + 1 = -7`. |

## 0.1 + 0.2 == 0.3
`0.1 + 0.2` gives `0.30000000000000004` so the comparison is `False`. 0.1 and 0.2 have no exact binary representation (like 1/3 in decimal), so each is stored as the nearest binary fraction, and the sum is one unit in the last place away from the stored 0.3. `Decimal(0.1)` shows the real stored value: `0.1000000000000000055511151231257827...`. `round(0.1 + 0.2, 2) == 0.3` is `True` and `Decimal('0.1') + Decimal('0.2') == Decimal('0.3')` is `True`.

## Why money must not be added as float rupees
Errors of ~1e-16 per addition accumulate. In the program of the assignment, 1,003 additions give `33400.30000000061` instead of `33400.30` (see `output_task02_complete.txt`). Alternatives: (1) integer paise, (2) `round()` after each addition, (3) the `decimal` module.

## Complete the Code
`total_decimal` creates `Decimal(amount)` from each **string** and adds. Output matches the expected output:
```
float  : 33400.30000000061
Decimal: 33400.30
False True
```
**Change `Decimal(amount)` to `Decimal(float(amount))`:** the total becomes `33400.29999999999857893118278` and no longer equals `33400.30`. `float("33.40")` is already the inexact binary number `33.39999999999999857891452847979962825775146484375`; `Decimal` then copies that inexact value *exactly*. Decimal is only exact when it is built from the decimal **string** (or an integer), never from a float.

## Alternative concept and complexity analysis
| Method | Idea | Time per addition | Memory per value (`sys.getsizeof`) | Exact for n payments? |
|---|---|---|---|---|
| Integer paise | parse `"33.40"` -> `3340`, add ints, divide by 100 only for display | O(1) (but needs parsing) | `int` 28 bytes | **Yes**, always (integers are exact) |
| float + `round(total, 2)` after every add | keep float, repair after each step | O(1) | `float` 24 bytes | Matched the integer-paise total in my runs for n = 300, 6,000, 150,000, but this is luck of rounding to the nearest double, not a guarantee; it also costs an extra `round()` per addition |
| `Decimal` from strings | exact decimal arithmetic | O(1), larger constant than float | `Decimal` 104 bytes | **Yes** |
| plain float | `total += float(a)` | O(1), fastest | 24 bytes | **No** (see the `False` rows in the output) |

All methods are O(n) for n payments and O(1) extra space (only the running total). Decimal values are about 4x bigger than a float. Integer paise needs hand-written parsing of every text amount, which was slower than `Decimal(text)` in my measurement and is more error-prone (every conversion to/from rupees must be written by hand); `Decimal` is the clearest, exact, and fast enough (Task 10). Use your own timings from `output_task02_alternatives.txt`.

Note: Python 3.12's built-in `sum()` for floats uses compensated summation and hides the error, so the demonstrations use an explicit `+=` loop like the assignment's `total_float()`.

## Evidence
`output_task02_session.txt`, `output_task02_complete.txt`, `output_task02_alternatives.txt` (below).

## Program output (as produced by my run)

### output_task02_alternatives.txt
```
1) The example of the assignment (1003 payments)
   int paise            : 3340030 paise = 33400.30
   float, no rounding   : 33400.30000000061
   float, round each add: 33400.3
   Decimal              : 33400.30

2) Memory per value (sys.getsizeof, bytes)
   float   33.4        : 24
   int     3340        : 28
   Decimal 33.40       : 104

3) Exactness and time for n payments (best of 3)
       n method                            total  exact?   time (s)
     300 int paise                      64904.14    True    0.00008
     300 float, no rounding     64904.140000000014   False    0.00001
     300 float, round each add          64904.14    True    0.00008
     300 Decimal                        64904.14    True    0.00004

    6000 int paise                    1227572.58    True    0.00171
    6000 float, no rounding     1227572.5800000029   False    0.00028
    6000 float, round each add        1227572.58    True    0.00175
    6000 Decimal                      1227572.58    True    0.00083

  150000 int paise                   30854055.16    True    0.03696
  150000 float, no rounding     30854055.159999833   False    0.00575
  150000 float, round each add       30854055.16    True    0.04894
  150000 Decimal                     30854055.16    True    0.02817

exact? = identical to the integer-paise total (the reference).
```

### output_task02_complete.txt
```
float  : 33400.30000000061
Decimal: 33400.30
False True

--- Change asked in the task: Decimal(float(amount)) ---
Decimal(float(amount)) total : 33400.29999999999857893118278
Equals 33400.30 ?            : False
Decimal(float('33.40'))      : 33.39999999999999857891452847979962825775146484375
```

### output_task02_session.txt
```
>>> type(10)
<class 'int'>
>>> type(10.0)
<class 'float'>
>>> type("10")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type([10, 8.5])
<class 'list'>
>>> isinstance(True, int)
True
>>> True + True
2
>>> 7 / 2
3.5
>>> 7 // 2
3
>>> 7 % 2
1
>>> -7 // 2
-4
>>> -7 % 2
1
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
>>> round(0.1 + 0.2, 2) == 0.3
True
>>> (4.2 - 3.5) / 0.1
7.000000000000002
>>> from decimal import Decimal
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')
>>> Decimal('0.1') + Decimal('0.2') == Decimal('0.3')
True
>>> Decimal(0.1)
Decimal('0.1000000000000000055511151231257827021181583404541015625')
>>> Decimal('0.1')
Decimal('0.1')
>>> int(33.40 * 100)
3340
>>> round(33.40 * 100)
3340
>>> '10' + 5
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task02_run1.png`.
