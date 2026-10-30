# Q7 - Diagnose, Redesign, Validate  (chosen program: Q6 recursive staircase)
import sys, time
from functools import lru_cache

calls = 0

def ways_naive(n):                      # ORIGINAL
    global calls; calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):                       # INTERMEDIATE (memoised)
    global calls; calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_loop(n):                       # REDESIGN: only last two values, O(1) space
    a = b = 1
    iterations = 0
    for _ in range(n - 1):
        a, b = b, a + b
        iterations += 1
    return b, iterations

print("n | naive calls | memo calls | loop iterations | naive time(s) | loop time(s)")
for n in (10, 20, 25, 30):
    calls = 0
    t = time.perf_counter(); r1 = ways_naive(n); tn = time.perf_counter() - t; cn = calls
    ways_memo.cache_clear(); calls = 0; r2 = ways_memo(n); cm = calls
    t = time.perf_counter(); r3, it = ways_loop(n); tl = time.perf_counter() - t
    assert r1 == r2 == r3
    print(f"{n} | {cn} | {cm} | {it} | {tn:.6f} | {tl:.8f}")

print("\nn = 1000")
ways_memo.cache_clear()
try:
    ways_memo(1000)
    print("memo at default limit: OK")
except RecursionError:
    print("memo at default limit (", sys.getrecursionlimit(), "): RecursionError")
r, it = ways_loop(1000)
print("loop: OK, iterations =", it, ", digits =", len(str(r)))
sys.setrecursionlimit(5000)
ways_memo.cache_clear()
print("loop == memo (limit raised):", r == ways_memo(1000))
