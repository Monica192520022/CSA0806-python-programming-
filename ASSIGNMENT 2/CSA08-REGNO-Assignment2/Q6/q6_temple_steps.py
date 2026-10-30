import sys, time
from functools import lru_cache
calls = 0
def ways_naive(n):
    global calls; calls += 1
    if n <= 1: return 1
    return ways_naive(n-1)+ways_naive(n-2)
@lru_cache(maxsize=None)
def ways_memo(n):
    global calls; calls += 1
    if n <= 1: return 1
    return ways_memo(n-1)+ways_memo(n-2)
def ways_loop(n):
    a=b=1
    for _ in range(n-1): a,b=b,a+b
    return b if n>=1 else 1
print([ways_naive(n) for n in range(1,7)])
print("n  naive_calls  memo_calls")
for n in (10,20,25,30):
    calls=0; ways_naive(n); cn=calls
    ways_memo.cache_clear(); calls=0; ways_memo(n); cm=calls
    print(n, cn, cm)
calls=0; print("naive:", ways_naive(25), "calls =", calls)
ways_memo.cache_clear(); calls=0; print("memo :", ways_memo(25), "calls =", calls)
print("limit", sys.getrecursionlimit())
ways_memo.cache_clear()
try: ways_memo(1000); print("memo 1000 OK")
except RecursionError as e: print("RecursionError:", e)
sys.setrecursionlimit(5000); ways_memo.cache_clear(); calls=0
r=ways_memo(1000); print("raised limit ok, calls", calls, "digits", len(str(r)))
print("loop equal:", ways_loop(1000)==r)
sys.setrecursionlimit(1000)
for n in (30,):
    s=time.perf_counter(); ways_naive(n); print("naive30 time", time.perf_counter()-s)
s=time.perf_counter(); ways_loop(1000); print("loop1000 time", time.perf_counter()-s)
