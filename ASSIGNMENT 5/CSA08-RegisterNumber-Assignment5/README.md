# CSA08 Assignment 5 (CO5) - Air-quality data: acquire, clean, store, analyse, AI

Name: ____________   Register number: ____________
Python 3.12, libraries in requirements.txt (pandas, matplotlib). Also used: csv, sqlite3, statistics, re, logging, cProfile.
The full report is REPORT (see the Claude document / your submitted file).

Run in this order (all commands inside this folder):
1. python make_data.py            creates data/raw_*.csv (4 stations, October 2026, with faults on purpose)
2. python clean.py                before / after on messy.csv (Task B1.1)
3. python complete_b1.py          Complete the Code B1
4. python pipeline.py             clean, store in airquality.db with executemany, three SQL questions (B1.3)
5. python charts.py               six charts in charts/ (B1.4)
6. python complete_b2.py          Complete the Code B2
7. python adversarial.py          bad files, SQL quote, tricky sentences (B2)
8. python b3_loops_pandas_sql.py  loops vs running sum vs pandas vs SQL for 1, 12, 120 stations (B3) - makes year_*.csv (26 MB, not committed)
9. python b3_profile.py           cProfile (B3.3)
10. python b4_index.py            index experiment (B4.2)
11. python complete_b4.py         Complete the Code B4
12. python ai_demo.py             sentiment agreement and summariser on 50 complaints (B4.1)
13. python chatbot.py             rule-based chatbot (A5.2)
14. python alt_naive_bayes.py     Naive Bayes alternative
15. python alt_experiments.py     measurements for the alternative-concept questions

outputs/ holds the text output of my own run. Replace or add your own screenshots, and commit after each task.
Add year_*.csv, big.db and profile.out to .gitignore (they are large and can be re-created).
