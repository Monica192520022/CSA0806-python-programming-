# Q3 – Dictionaries – Kisan complaints (7)

Write your report answers here (design, analysis, tables, conclusions).

## Implementation
- [ ] Word frequency using get() and setdefault()
- [ ] Group complaints by district (dict of lists)
- [ ] Top-k sorted by count desc then alphabetical
- [ ] Stop words via set
## Design & Analysis
- [ ] How dict finds a key (hashing), why O(1) average
- [ ] dict vs list.count() per distinct word
- [ ] Key order in Python 3.7+
- [ ] keys()/values()/items() views
## Experiments
- [ ] 1,000 / 10,000 / 100,000 complaints: dict vs list.count() vs Counter
- [ ] Empty text, upper/lower case, punctuation
## Engineering decision (100,000/day)
## Complete the Code (q3_complete_code.py)
- [ ] TODO 1 & 2, output matches; explain why 'price' before 'received'
## Alternative: list.count() O(n·d) / Counter O(n)
