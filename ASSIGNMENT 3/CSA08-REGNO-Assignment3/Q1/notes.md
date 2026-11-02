# Q1 – Lists and Slicing – Rainfall (6)

Write your report answers here (design, analysis, tables, conclusions).

## Implementation
- [ ] 365-value list, weekly totals via slicing
- [ ] max/min with positions (wettest/driest week too)
- [ ] 7-day moving average
- [ ] dry days list (0 mm)
## Design & Analysis
- [ ] Pseudocode for moving average
- [ ] What `readings[7:14]`, `readings[-7:]`, `readings[::7]` return
- [ ] Why list is suitable; cost of append / insert / pop / sort
- [ ] Derive additions: naive (~7(n-6)) vs running sum (~n)
## Experiments
- [ ] 365 / 36,500 / 365,000 readings, time naive vs running sum, compare with counts
- [ ] Test empty list and list shorter than 7
## Design question
- [ ] Cost of list.insert() (O(n)); would you still use a list?
## Alternative concept
- [ ] deque(maxlen=7) / dict keyed by date; time O(7n) vs O(n); space
