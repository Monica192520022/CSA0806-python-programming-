import random, time

def weekly_totals(readings):
    # TODO: use slicing readings[i:i+7]
    pass

def max_min_with_positions(readings):
    # TODO: return (max_val, max_idx, min_val, min_idx)
    pass

def moving_avg_naive(readings, w=7):
    # TODO: sum(readings[i:i+w]) / w for each window
    pass

def moving_avg_running(readings, w=7):
    # TODO: running sum: add new, subtract old
    pass

def dry_days(readings):
    # TODO: indices where reading == 0
    pass

def experiment():
    for n in (365, 36_500, 365_000):
        data = [random.choice([0, 0, round(random.uniform(0.1, 60), 1)]) for _ in range(n)]
        # TODO: time both moving averages with time.perf_counter()
        # TODO: compare with derived addition counts

def edge_cases():
    # TODO: empty list, list shorter than 7
    pass

if __name__ == "__main__":
    random.seed(1)
    readings = [random.choice([0, 0, round(random.uniform(0.1, 60), 1)]) for _ in range(365)]
    # TODO: call your functions and print results
    experiment()
    edge_cases()
    # TODO (alternative): deque(maxlen=7) version
