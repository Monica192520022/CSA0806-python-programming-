calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP = {"not", "high"}


def frequencies(texts, stop):
    # TODO 1: Return a dictionary word -> count for every word that is not in stop,
    #   using dict.get()
    pass  # replace this line with your code


def top(counts, k):
    # TODO 2: Return the k most frequent (word, count) pairs, highest count first and
    #   alphabetical for ties
    pass  # replace this line with your code


print(top(frequencies(calls, STOP), 3))
# Expected: [('seeds', 3), ('price', 2), ('received', 2)]
