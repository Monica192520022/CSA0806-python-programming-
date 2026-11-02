# Q7 – Contact Merging from First Principles (10)

Write your report answers here (design, analysis, tables, conclusions).

## Stage 1 – Interpret (2)
- [ ] Input, output, same-person rules
- [ ] Data structures needed
- [ ] Measurable requirements
## Stage 2 – Design (3)
- [ ] Normalise numbers (strip spaces/+91/etc.) and names
- [ ] Merge via dict keyed by normalised number, sets for numbers & emails
- [ ] Pseudocode
## Stage 3 – Implement & Measure (3)
- [ ] Tests: duplicates, missing fields, formats
- [ ] Time at 1,000 and 100,000 contacts
- [ ] Hand-verified small case
## Stage 4 – Defend (2)
- [ ] Dict vs all-pairs; same-name different people; one limitation
## Alternative: all-pairs O(n²) vs dict O(n), with measurements
