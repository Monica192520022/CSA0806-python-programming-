# b3_profile.py - cProfile of the plain Python version (12 stations)
import cProfile
import pstats
from b3_loops_pandas_sql import method_loops

cProfile.run('method_loops("year_12.csv")', "profile.out")
stats = pstats.Stats("profile.out")
stats.sort_stats("cumulative").print_stats(8)
