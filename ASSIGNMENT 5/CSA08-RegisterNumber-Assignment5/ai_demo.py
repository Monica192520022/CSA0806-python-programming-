# ai_demo.py - Task B4.1: sentiment agreement and summariser on the complaints
import re
import time
from complaints import COMPLAINTS, LONG
from sentiment import label

# 1. agreement between the scorer and my own reading
agree = 0
wrong = []
for text, mine in COMPLAINTS:
    guess = label(text)
    if guess == mine:
        agree += 1
    else:
        wrong.append((guess, mine, text))
print("Agreement:", agree, "of", len(COMPLAINTS), "=", round(100 * agree / len(COMPLAINTS)), "%")
for g, m, t in wrong:
    print("  scorer:", g.ljust(8), "me:", m.ljust(8), "|", t)

# 2. extractive summariser: choose the sentences with the most frequent important words
STOP = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "to", "of", "in", "on", "at", "for", "i", "my",
        "it", "this", "that", "me", "we", "you", "please", "sir", "not", "has", "have", "had", "from", "with",
        "every", "near", "all", "no", "but", "so", "as", "be", "by", "am", "can", "will", "do", "does", "did"}


def split_sentences(text):
    return [s.strip() for s in re.split(r"[.!?]", text) if s.strip() != ""]


def summarise(text, k=1):
    sentences = split_sentences(text)
    counts = {}
    for w in re.findall(r"[a-z]+", text.lower()):
        if w not in STOP:
            counts[w] = counts.get(w, 0) + 1
    scores = []
    for i, s in enumerate(sentences):
        total = 0
        for w in re.findall(r"[a-z]+", s.lower()):
            if w not in STOP:
                total += counts[w]
        scores.append((total, i))
    best = sorted(scores, reverse=True)[:k]            # k highest scoring sentences
    chosen = sorted(i for _, i in best)                # keep the original order
    return ". ".join(sentences[i] for i in chosen) + "."


def first_k(text, k=1):
    return ". ".join(split_sentences(text)[:k]) + "."


print("\nExample complaint:")
print("  ", LONG[0][0])
print("   frequency summary:", summarise(LONG[0][0]))
print("   first-sentence   :", first_k(LONG[0][0]))
hits_freq = sum(1 for text, topic in LONG if topic in summarise(text).lower())
hits_first = sum(1 for text, topic in LONG if topic in first_k(text).lower())
print("Summaries that contain the main problem word (10 long complaints): frequency method", hits_freq,
      "| first sentence", hits_first)

# time per complaint
texts = [t for t, _ in LONG] * 2000
start = time.perf_counter()
for t in texts:
    summarise(t)
t1 = time.perf_counter() - start
start = time.perf_counter()
for t in texts:
    first_k(t)
t2 = time.perf_counter() - start
print("Time per complaint: frequency", round(t1 / len(texts) * 1e6, 1), "us | first-k", round(t2 / len(texts) * 1e6, 1), "us")
texts = [t for t, _ in COMPLAINTS] * 1000
start = time.perf_counter()
for t in texts:
    label(t)
print("Sentiment scorer:", round((time.perf_counter() - start) / len(texts) * 1e6, 1), "us per complaint")
