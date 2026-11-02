# Q2 – Tuples, Mutability, Copying – Bus stops (7)

Write your report answers here (design, analysis, tables, conclusions).

## Implementation
- [ ] Stops as tuples, used as dict keys
- [ ] Zone grid via list comprehension
- [ ] Aliasing, shallow copy (copy.copy, slicing), deep copy
- [ ] Tuple unpacking in for loop
## Design & Analysis
- [ ] Why tuples hashable, lists not
- [ ] Memory diagram of [[0]*3]*3 vs corrected grid
- [ ] Shallow vs deep copy: when each
- [ ] Why function changes caller's list
## Experiments
- [ ] Bug/fix with `is` and `id()`
- [ ] sys.getsizeof list vs tuple of 1,000,000
- [ ] Time creating + indexing tuple vs list
- [ ] Mutate a list inside a tuple, explain
## Complete the Code (q2_complete_code.py)
- [ ] TODO 1 done, output matches expected
- [ ] Try list as dict key, explain TypeError
## Conclusion + Alternative (dict keyed by (row,col), sparse)
