# alt_naive_bayes.py - a small Naive Bayes classifier written from scratch,
# tested with leave-one-out on the same 50 complaints
import math
import sys
import time
from complaints import COMPLAINTS
from sentiment import label


def words_of(text):
    return text.lower().replace(".", " ").replace(",", " ").split()


def train(data):
    word_counts = {"positive": {}, "negative": {}, "neutral": {}}
    class_counts = {"positive": 0, "negative": 0, "neutral": 0}
    vocab = set()
    for text, lab in data:
        class_counts[lab] += 1
        for w in words_of(text):
            word_counts[lab][w] = word_counts[lab].get(w, 0) + 1
            vocab.add(w)
    return word_counts, class_counts, vocab


def predict(model, text):
    word_counts, class_counts, vocab = model
    total = sum(class_counts.values())
    best, best_score = None, None
    for lab in class_counts:
        score = math.log((class_counts[lab] + 1) / (total + 3))
        size = sum(word_counts[lab].values())
        for w in words_of(text):
            score += math.log((word_counts[lab].get(w, 0) + 1) / (size + len(vocab)))     # add-one smoothing
        if best_score is None or score > best_score:
            best, best_score = lab, score
    return best


right = 0
for i in range(len(COMPLAINTS)):
    training = COMPLAINTS[:i] + COMPLAINTS[i + 1:]
    model = train(training)
    if predict(model, COMPLAINTS[i][0]) == COMPLAINTS[i][1]:
        right += 1
print("Naive Bayes (leave-one-out) accuracy:", right, "of 50 =", round(100 * right / 50), "%")
lex = sum(1 for t, l in COMPLAINTS if label(t) == l)
print("Word-list scorer accuracy           :", lex, "of 50 =", round(100 * lex / 50), "%")

model = train(COMPLAINTS)
start = time.perf_counter()
for i in range(2000):
    for t, _ in COMPLAINTS[:5]:
        predict(model, t)
print("Naive Bayes time per complaint:", round((time.perf_counter() - start) / 10000 * 1e6, 1), "us")
size = sys.getsizeof(model[2]) + sum(sys.getsizeof(d) for d in model[0].values())
print("Model size: vocabulary", len(model[2]), "words, about", size, "bytes (dictionaries only)")
