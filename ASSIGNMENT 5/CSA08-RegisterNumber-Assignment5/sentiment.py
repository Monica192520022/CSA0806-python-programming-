# sentiment.py - the lexicon based scorer (same logic as complete_b4.py), importable
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for i in range(len(words)):
        value = 0
        if words[i] in POSITIVE:
            value = 1
        elif words[i] in NEGATIVE:
            value = -1
        if value != 0 and i > 0 and words[i - 1] in NEGATORS:
            value = -value
        total = total + value
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"
