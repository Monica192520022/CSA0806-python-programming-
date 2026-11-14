import re
import sqlite3
import time
import random
from collections import Counter

POSITIVE = {"good", "clean", "fast", "helpful", "improved", "fresh", "clear", "safe", "pleasant", "responsive"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken", "dust", "smog", "toxic", "choking", "delay", "odor", "fumes"}
NEGATORS = {"not", "never", "no"}
STOPWORDS = {"the", "is", "are", "was", "were", "in", "on", "at", "to", "for", "of", "and", "a", "an", "it", "this", "that", "very", "with"}

def score_sentiment(text):
    words = re.sub(r"[^a-z0-9\s]", " ", text.lower()).split()
    total = 0
    for i, w in enumerate(words):
        val = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if val != 0 and i > 0 and words[i - 1] in NEGATORS:
            val = -val
        total += val
    return "positive" if total > 0 else "negative" if total < 0 else "neutral"

def extractive_summary(complaints, top_k=3):
    # Frequency-based extractive summariser across complaint corpus
    word_freq = Counter()
    all_sentences = []
    for comp in complaints:
        sents = [s.strip() for s in re.split(r"[.!?]+", comp) if s.strip()]
        for s in sents:
            all_sentences.append(s)
            tokens = [w for w in re.sub(r"[^a-z0-9\s]", " ", s.lower()).split() if w not in STOPWORDS and len(w) > 2]
            word_freq.update(tokens)

    scored = []
    for idx, s in enumerate(all_sentences):
        tokens = [w for w in re.sub(r"[^a-z0-9\s]", " ", s.lower()).split() if w not in STOPWORDS and len(w) > 2]
        if not tokens:
            continue
        s_score = sum(word_freq[w] for w in tokens) / (len(tokens) ** 0.5)
        scored.append((s_score, idx, s))

    top_sents = sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]
    top_sents.sort(key=lambda x: x[1])
    return [s for _, _, s in top_sents]

def first_k_summary(complaints, top_k=3):
    # Alternative Concept: Simply pick first k sentences
    all_sentences = []
    for comp in complaints:
        sents = [s.strip() for s in re.split(r"[.!?]+", comp) if s.strip()]
        all_sentences.extend(sents)
    return all_sentences[:top_k]

# 50 realistic citizen complaints with human ground-truth labels
COMPLAINTS_50 = [
    ("Heavy black smoke from the industrial estate near Guindy. Breathing is choking.", "negative"),
    ("Air feels much cleaner today after the morning rain in Adyar.", "positive"),
    ("The monitoring display board at T Nagar is broken and showing no data.", "negative"),
    ("App response was fast and the helpline staff were very helpful.", "positive"),
    ("Thick dust and fumes near the metro construction site.", "negative"),
    ("Not bad at all today, visibility has improved near the beach.", "positive"),
    ("Terrible burning garbage smoke every night in Velachery.", "negative"),
    ("Good initiative by the board, air quality alerts are clear and timely.", "positive"),
    ("The sensor station was never repaired despite three complaints.", "negative"),
    ("Fresh breeze and clean air in Anna Nagar park this morning.", "positive"),
    ("Traffic smog in Koyambedu is making eyes burn.", "negative"),
    ("Complaint resolution was slow and the officer on duty was rude.", "negative"),
    ("Air quality has improved significantly over the last week.", "positive"),
    ("Toxic chemical odor leaking near Perambur railway yard.", "negative"),
    ("Very pleasant and clear sky today across Besant Nagar.", "positive"),
    ("No action taken on the open waste burning report.", "negative"),
    ("The new mobile app update is fast and clean.", "positive"),
    ("Choking diesel fumes from idling buses at the depot.", "negative"),
    ("Staff were not helpful when asked about local AQI readings.", "negative"),
    ("Safe and clean environment maintained around the school zone.", "positive"),
    ("Dust clouds from uncovered lorries are dirtying the whole street.", "negative"),
    ("The helpline team responded fast and resolved the sensor glitch.", "positive"),
    ("Smog levels look really bad near the highway junction.", "negative"),
    ("Not dirty anymore, the road sweeping trucks did a good job.", "positive"),
    ("Broken air purifier kiosk at the bus terminus.", "negative"),
    ("Clear morning air and good visibility across the river bridge.", "positive"),
    ("Industrial smoke continues unabated after midnight.", "negative"),
    ("The dashboard charts are clear and helpful for citizens.", "positive"),
    ("Slow response from the pollution control zone office.", "negative"),
    ("Clean streets and fresh air after strict construction dust rules.", "positive"),
    ("Bad odor and thick fumes near the canal.", "negative"),
    ("Service has improved a lot this month.", "positive"),
    ("No helpful information provided on the website.", "negative"),
    ("Factory smoke is causing severe throat irritation.", "negative"),
    ("Good and fast inspection by the field team.", "positive"),
    ("Dirty air and heavy dust near the quarry road.", "negative"),
    ("The air is not bad today compared to yesterday.", "positive"),
    ("Rude behavior by the contractor dumping debris.", "negative"),
    ("Clear skies and pleasant weather in the evening.", "positive"),
    ("Broken pipeline releasing foul odor.", "negative"),
    ("Helpful alerts warned us before the smog peak.", "positive"),
    ("Traffic fumes are choking pedestrians every evening.", "negative"),
    ("Clean and safe walking track near the lake.", "positive"),
    ("Never seen such thick smoke in this residential area.", "negative"),
    ("Fast action on illegal brick kiln smoke.", "positive"),
    ("Dust and broken footpaths make commuting terrible.", "negative"),
    ("Air quality is good and fresh near the botanical garden.", "positive"),
    ("Slow app loading and broken map pins.", "negative"),
    # 2 adversarial/tricky complaints where simple lexicon struggles
    ("Oh great, more factory smoke, truly a wonderful gift for our lungs.", "negative"),
    ("The air is not never polluted near the junction.", "negative"),
]

if __name__ == "__main__":
    # B4.1 Evaluate Sentiment Scorer & Summariser on 50 complaints
    texts = [c[0] for c in COMPLAINTS_50]
    truth = [c[1] for c in COMPLAINTS_50]
    preds = [score_sentiment(t) for t in texts]
    matches = sum(1 for p, y in zip(preds, truth) if p == y)

    print(f"--- B4.1 Evaluation on {len(COMPLAINTS_50)} Citizen Complaints ---")
    print(f"Agreement with Human Labels: {matches}/{len(COMPLAINTS_50)} ({matches/len(COMPLAINTS_50)*100:.1f}%)")
    print("\nFrequency-Based Extractive Summary (Top 3 Sentences):")
    for idx, s in enumerate(extractive_summary(texts, top_k=3), 1):
        print(f"  {idx}. {s}")

    print("\nAlternative (First-k Sentences) Summary:")
    for idx, s in enumerate(first_k_summary(texts, top_k=3), 1):
        print(f"  {idx}. {s}")

    # B4.2 Index Impact Measurement at Scaled Volume (112 stations x 15-min intervals for 30 days = 322,560 rows)
    print("\n--- B4.2 SQLite Composite Index (station, day) Benchmark ---")
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings_scale (station TEXT, day TEXT, slot INTEGER, pm25 REAL)")
    random.seed(7)
    scaled_rows = [
        (f"Station_{s:03d}", f"2026-10-{d:02d}", slot, round(random.uniform(20, 190), 2))
        for s in range(1, 113)
        for d in range(1, 31)
        for slot in range(96)
    ]
    con.executemany("INSERT INTO readings_scale VALUES (?, ?, ?, ?)", scaled_rows)
    con.commit()

    query = "SELECT AVG(pm25), MIN(pm25), MAX(pm25) FROM readings_scale WHERE station = 'Station_085' AND day = '2026-10-18'"

    # Time without index (average over 50 runs)
    t0 = time.perf_counter()
    for _ in range(50):
        con.execute(query).fetchone()
    t_no_idx = (time.perf_counter() - t0) / 50

    # Create composite index on (station, day)
    con.execute("CREATE INDEX idx_station_day ON readings_scale(station, day)")
    con.commit()

    t0 = time.perf_counter()
    for _ in range(50):
        con.execute(query).fetchone()
    t_with_idx = (time.perf_counter() - t0) / 50
    con.close()

    print(f"Total Rows: {len(scaled_rows):,}")
    print(f"Avg Query Time WITHOUT Index : {t_no_idx*1000:.3f} ms")
    print(f"Avg Query Time WITH Index    : {t_with_idx*1000:.3f} ms")
    print(f"Speedup Factor               : {t_no_idx / t_with_idx:.1f}x faster")
