# Task 3 - Choose Variables and Name the Constants (K3)

Run: `python task03_constants.py`

## The constants (single place for every rate)
```python
BASE_RATE      = 30.00   # Rs per litre at 3.5 % fat and 8.5 % SNF
FAT_STEP_VALUE = 0.40    # Rs per litre per 0.1 % fat
SNF_STEP_VALUE = 0.30    # Rs per litre per 0.1 % SNF
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1
```
A rate revision = edit one line.

## Naming rules and conventions
* A name starts with a letter or `_`, then letters, digits or `_`; no spaces or `-`; cannot be a keyword (`class`). The program tests this with `str.isidentifier()` and `keyword.iskeyword()`: `2fat`, `fat-percent`, `class` are invalid.
* `snake_case` for variables and functions (`fat_steps`), `UPPER_CASE` for constants (`BASE_RATE`), meaningful names (`litres`, not `x`). Names are case sensitive.

## Python has no true constants
Re-assigning `BASE_RATE = 99.0` runs without any error (shown in the output). `typing.Final` only helps a type checker such as mypy; the interpreter ignores it. So constants are a **convention**: UPPER_CASE names that nobody assigns after the definition. For real protection a read-only mapping such as `types.MappingProxyType` refuses changes (`TypeError`).

## Dynamic typing
A name has no fixed type; the *object* has one. `x = 8` (int) and later `x = "eight"` (str) is legal. The error only appears when an invalid operation runs (`10 + "5"` -> `TypeError`). Consequence for the clerk's program: a value that was typed as text must be converted before arithmetic (Task 5).

## Multiple assignment and swapping
`fat, snf = 3.5, 8.5`, then `fat, snf = snf, fat` swaps without a temporary variable (the right side is evaluated completely first). `a = b = 0` gives both names the same value.

## Alternative concept and complexity analysis
Three solutions for the rates:
1. **Magic numbers** - `30.0`, `0.40`, `0.30` typed in each expression.
2. **Dictionary** - `RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}`.
3. **Named constants** (chosen).

| | Places to change for a revision | Time | Memory |
|---|---|---|---|
| Magic numbers | **k places** (the program counts 3 copies of `0.40` in just 3 small functions; a real program has more, and a place that is missed gives a partial revision - the original bug) | O(1) per rate calculation | O(1) |
| Dictionary | 1 place; also handy for passing the whole card to a function | O(1) per lookup (hash lookup), slightly slower than a global name (measured) | O(1): one dict object |
| Named constants | 1 place | O(1) | O(1): three names |

The running time and memory are the same order O(1) per calculation; the measured difference is a fraction of a second for 300,000 calls. The real difference is **maintainability**: k edits (error-prone) versus one.

## Evidence
`output_task03_constants.txt` (below).

## Program output (as produced by my run)

### output_task03_constants.txt
```
1) Naming rules
   'fat'              valid identifier? True
   'fat_percent'      valid identifier? True
   'FAT_STEP_VALUE'   valid identifier? True
   '2fat'             valid identifier? False
   'fat-percent'      valid identifier? False
   'class'            valid identifier? False
   '_total'           valid identifier? True
   Convention: snake_case for variables/functions, UPPER_CASE for constants.

2) Python has no true constants
   BASE_RATE before: 30.0
   BASE_RATE after re-assignment: 99.0 (no error!)
   read-only mapping (MappingProxyType) refuses change -> 'mappingproxy' object does not support item assignment

3) Dynamic typing
   x = 8 -> int
   x = eight -> str (same name, new type, no error)
   TypeError only when the operation is executed -> unsupported operand type(s) for +: 'int' and 'str'

4) Multiple assignment and swapping
   before: 3.5 8.5
   after a, b = b, a : 8.5 3.5
   a = b = 0 -> 0 0

5) Alternative: magic numbers vs constants vs dictionary
   places holding the number 0.40 in the magic-number design: 3
   places holding the number 0.40 in the constants design   : 1 (FAT_STEP_VALUE)
   places holding the number 0.40 in the dictionary design  : 1 (RATE_CARD['fat'])
   results equal for (4.2, 8.7): 33.4 33.4 33.4
   constants      300000 calls: 0.145 s
   magic numbers  300000 calls: 0.093 s
   dictionary     300000 calls: 0.101 s
   Memory: constants = 3 names, dictionary = 1 dict object; both O(1).
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task03_run1.png`.
