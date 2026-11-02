import random, time, sys

def clean_loop(readings):
    # TODO: for loop + append; keep -50 <= c <= 50, also convert to F = c*9/5+32
    pass

def clean_comprehension(readings):
    pass  # TODO

def clean_map_filter(readings):
    pass  # TODO: map() + filter() + lambda

def alarm_minutes(readings):
    pass  # TODO: enumerate(), minutes with temp outside 2..8

def experiment():
    for n in (10_000, 100_000, 1_000_000):
        pass  # TODO: time the 3 versions; getsizeof list vs generator

if __name__ == "__main__":
    # TODO: verify all 3 give identical results; all-valid / all-invalid tests
    # TODO: dict comprehension, set comprehension examples
    # TODO: generator version: sum(c for c in readings if -50 <= c <= 50)
    experiment()
