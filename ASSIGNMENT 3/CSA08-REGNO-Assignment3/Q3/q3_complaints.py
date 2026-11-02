import random, time, string
from collections import Counter

STOP_WORDS = {"not", "high", "the", "is", "a", "and"}

def clean(text):
    # TODO: lowercase + strip punctuation
    pass

def count_with_get(texts): pass          # TODO: dict.get()
def count_with_setdefault(texts): pass   # TODO: setdefault()
def count_with_list_count(texts): pass   # TODO: list.count() per distinct word
def count_with_counter(texts): pass      # TODO: collections.Counter
def group_by_district(records): pass     # TODO: dict of lists
def top_k(counts, k): pass               # TODO: sort by (-count, word)

def experiment():
    for n in (1_000, 10_000, 100_000):
        pass  # TODO: generate n complaints, time the 3 methods

if __name__ == "__main__":
    # TODO: tests - empty text, mixed case, punctuation
    experiment()
