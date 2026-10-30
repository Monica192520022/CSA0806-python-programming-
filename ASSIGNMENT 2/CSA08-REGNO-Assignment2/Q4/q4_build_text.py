# Q4 - Complete the Code (TODO 1). Run 3 times and average.
import time

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]

def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text

def build_join(parts):
    # TODO 1 done: single str.join() call (trailing ";" so text equals build_plus)
    return ";".join(parts) + ";"

plus_times, join_times = [], []
for run in range(3):
    start = time.perf_counter(); a = build_plus(items); t_plus = time.perf_counter() - start
    start = time.perf_counter(); b = build_join(items); t_join = time.perf_counter() - start
    plus_times.append(t_plus); join_times.append(t_join)
    print(f"run {run+1}: same text: {a == b} | length: {len(b)}")
    print(f"        += time: {t_plus:.4f} s   join time: {t_join:.4f} s")

print(f"AVERAGE of 3 runs: += {sum(plus_times)/3:.4f} s | join {sum(join_times)/3:.4f} s")
