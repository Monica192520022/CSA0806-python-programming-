# Q6 – Nested Data – Railway timetable (7)

Write your report answers here (design, analysis, tables, conclusions).

## Implementation
- [ ] timetable dict: train_no -> {name, stops[(station, arr, dep)], days:set}, >=5 trains
- [ ] Trains stopping at station on a day
- [ ] sorted() with key=lambda by departure
- [ ] Neat printing
## Design & Analysis
- [ ] Diagram + expression for departure of 3rd station
- [ ] Why dict / list / tuple / set for each part
- [ ] Work per station query; station->trains index design
## Experiments
- [ ] 100 / 1,000 / 10,000 trains: with vs without index
- [ ] Unknown station; train not running that day
- [ ] Extra memory of index
## Conclusion + Alternative (flat list of tuples, O(total stops))
