# Task 8 - Plan the Algorithm Before Coding (K3)

Files: `pseudocode.md` (pseudocode + flowchart + hand trace), `task08_algorithm.py` (program that reproduces the hand trace and measures the alternatives)

Run: `python task08_algorithm.py`

## Steps of algorithmic problem solving
1. **Understand** - inputs, outputs, rules (Task 1).
2. **Plan** - pseudocode and flowchart *before* any Python (`pseudocode.md`).
3. **Write** - translate the plan into Python (Task 9).
4. **Test** - compare with the hand trace and with test cases (Tasks 8-9).

See `pseudocode.md` for the pseudocode, the validation flowchart and the hand trace of three entries. The program's table in `output_task08_algorithm.txt` shows the same intermediate values (steps, rate, amount, running total) as the hand trace, which proves that pseudocode and program match.

> Format note: the pseudocode follows the common structure (ALGORITHM / INPUT / OUTPUT / BEGIN ... END, upper-case keywords, indentation, `<-` for assignment). If your college template (SIMATS Engineering - Standard for Algorithmic Pseudocode) differs, only change the keywords/layout; the logic is the same.

## Alternative concept and complexity analysis
* **Store every payment in a list and add at the end:** `amounts.append(...)` n times, then `sum(amounts)`.
* **Keep a running total while reading:** `total += amount`.

| | Store then add | Running total |
|---|---|---|
| Time | O(n) (n payments + n additions) | O(n) |
| Space | **O(n)** | **O(1)** |
| Measured peak memory (n = 300 / 6,000 / 150,000) | about 37 KB / 665 KB / 16.5 MB | 4 KB for every n |

Both give the same total (shown in the output). Storing is still necessary when the amounts must be used again: printing the farmer's statement, sorting or searching payments, finding the largest payment, correcting one entry, or auditing the total. If only the total is needed, the running total is the better design, and it matters at district-union size (150,000 farmers).
(Times in this program are larger than elsewhere because `tracemalloc` slows Python while measuring memory.)

## Evidence
`output_task08_algorithm.txt` (below) and `pseudocode.md`.

## Program output (as produced by my run)

### output_task08_algorithm.txt
```
1) Hand trace of the pseudocode for three entries (compare with Task08/pseudocode.md)
    i  litres   fat   snf fat_steps snf_steps    rate   amount     total
    1      10   3.5   8.5         0         0   30.00   300.00    300.00
    2     8.5   4.2   8.7         7         2   33.40   283.90    583.90
    3      12   3.1   8.3        -4        -2   27.80   333.60    917.50
   ten_day_total = 917.50

2) ALTERNATIVE: store every amount in a list, or keep a running total
          n method                      total  time (s)  peak memory (KB)
        300 store then add         1569055.10    0.0043              36.7
        300 running total          1569055.10    0.0043               4.0
       6000 store then add        31613349.86    0.0892             665.0
       6000 running total         31613349.86    0.0810               4.0
     150000 store then add       791694865.85    3.0991           16491.2
     150000 running total        791694865.85    3.0712               4.0
   Same total, same O(n) time; peak memory grows with n only for 'store then add'.
   Storing is still needed when the amounts must be printed again, sorted, or audited.
```

## Screenshots
Put your own screenshots of each run in the `screenshots/` folder of this task and name them like `Task08_run1.png`.
