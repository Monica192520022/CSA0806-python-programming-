# PART A – DATA AND PROGRAM DESIGN (25 Marks)
**Standard:** All pseudocode follows the SIMATS Engineering – Standard for Algorithmic Pseudocode (`ALGORITHM`, `INPUT`, `OUTPUT`, `BEGIN`, `END`, `<-`, uppercase control structures).

---

## TASK A1 – DESIGN THE DATA ACQUISITION (7 Marks)

### A1.1 – Inspect the Source
Each of the 12 monitoring stations generates a daily CSV file (e.g., `station_adyar_20261001.csv`) containing hourly sensor telemetry.
- **Expected CSV Structure:**
  `station_name,date,hour,pm25,pm10,no2,temperature`
  - `station_name` (String): Name or code of the monitoring station.
  - `date` (String): Observation date.
  - `hour` (Integer, 0–23): Hour of the day.
  - `pm25` (Float): Fine particulate matter ($\mu g/m^3$).
  - `pm10` (Float): Coarse particulate matter ($\mu g/m^3$).
  - `no2` (Float): Nitrogen dioxide ($\mu g/m^3$).
  - `temperature` (Float): Ambient air temperature.

- **Expected Data-Quality Problems & Examples:**
  1. **Missing Values:** Blank fields, `"NA"`, `"NULL"`, or `"NaN"` due to telemetry dropouts (e.g., `Adyar,2026-10-01,14,NA,88.2,31.0,30.5` or `Adyar,2026-10-01,15,,90.1,32.4,31.0`).
  2. **Impossible / Out-of-Range Sensor Values:** Negative concentrations or hardware saturation spikes (e.g., `Guindy,2026-10-01,09,-12.4,45.0,18.2,29.0` or `Guindy,2026-10-01,10,9999.0,120.5,40.1,30.2`).
  3. **Inconsistent Temperature Units:** Two stations report temperature in Fahrenheit ($^\circ F$) instead of Celsius ($^\circ C$) (e.g., `AnnaNagar,2026-10-01,12,55.2,98.0,28.5,89.6`).
  4. **Duplicate Rows:** Repeated transmissions of the same `(station_name, date, hour)` tuple due to network retries.
  5. **Inconsistent Date & String Formatting:** Mixed date formats (`01-10-2026` vs `2026/10/01` vs `2026-10-01`) and trailing whitespace or inconsistent casing in station names (`" adyar "` vs `"Adyar"`).

### A1.2 – Design the Storage (SQLite Schema)
A normalised two-table relational schema avoids repeating station metadata across millions of hourly rows and enforces referential integrity.

1. **`stations` Table:**
   - `station_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
   - `station_name` (`TEXT NOT NULL UNIQUE`)
   - `zone` (`TEXT`)
   - `temp_unit` (`TEXT CHECK(temp_unit IN ('C', 'F')) DEFAULT 'C'`)

2. **`readings` Table:**
   - `reading_id` (`INTEGER PRIMARY KEY AUTOINCREMENT`)
   - `station_id` (`INTEGER NOT NULL`, Foreign Key referencing `stations(station_id)`)
   - `obs_date` (`TEXT NOT NULL`, ISO-8601 `YYYY-MM-DD`)
   - `obs_hour` (`INTEGER NOT NULL CHECK(obs_hour BETWEEN 0 AND 23)`)
   - `pm25` (`REAL`)
   - `pm10` (`REAL`)
   - `no2` (`REAL`)
   - `temp_c` (`REAL`)
   - `pm25_minmax` (`REAL`)
   - `pm25_zscore` (`REAL`)
   - **Composite Unique Constraint:** `UNIQUE(station_id, obs_date, obs_hour)` to prevent duplicate hourly entries at the database level.

- **CSV-to-SQLite Mapping:**
  The CSV `station_name` is stripped and title-cased, then looked up in `stations` to resolve `station_id`. `date` maps to `obs_date` (standardised to `YYYY-MM-DD`), `hour` maps to `obs_hour` (integer), pollutant columns map directly to `REAL` columns, and `temperature` is converted to Celsius before mapping to `temp_c`.

### A1.3 – CSV or SQL Comparison
| Typical Board Question | Reading Raw CSV Files | Querying SQLite Database |
| :--- | :--- | :--- |
| **1. Average PM2.5 of one station (Adyar) in October** | Must open 31 daily files, parse every line linearly, filter `station == 'Adyar'` and `date` prefix, and accumulate sum/count in Python. | Single declarative query: `SELECT AVG(pm25) FROM readings JOIN stations USING(station_id) WHERE station_name='Adyar' AND obs_date LIKE '2026-10-%';` |
| **2. Top 5 hours with worst NO2 across all stations** | Must load all 360+ CSVs into memory simultaneously and run a global sort across every record. | Uses `ORDER BY no2 DESC LIMIT 5;` directly in SQLite without loading non-matching columns into Python objects. |
| **3. Daily min, max, and mean PM10 per station** | Requires nested dictionaries `(station, date) -> list` and manual aggregation loops in Python. | Computed natively inside the SQLite C engine via `GROUP BY station_id, obs_date`. |

### Alternative Concept & Complexity Analysis (CSV + Pandas DataFrame per Query vs SQLite)
- **Alternative Approach:** Keep all data in daily CSV files and load them into a `pandas.DataFrame` (`pd.concat([pd.read_csv(f) for f in files])`) every time a question is asked.
- **Time Complexity per Question:**
  - **CSV + Pandas (without persistent index):** Every query requires reading $n$ rows from disk, parsing text into floating-point arrays, and scanning $n$ rows to filter: **$O(n)$** I/O and CPU time per query.
  - **SQLite with B-Tree Index on `(station_id, obs_date)`:** Data is parsed once during ingestion. Locating a specific station and date range traverses a B-Tree index in **$O(\log n + k)$** time (where $k$ is the number of matching rows), avoiding a full table scan.
- **Space Complexity (Disk vs Memory):**
  - **CSV + Pandas:** CSV text is verbose on disk, and `pandas` must allocate contiguous RAM for the entire dataset ($O(n)$ memory) during every query, risking `MemoryError` as years of data accumulate.
  - **SQLite:** Stores compact binary pages on disk and streams query results using a small fixed page cache ($O(1)$ auxiliary working memory for simple aggregations).

---

## TASK A2 – DESIGN THE CLEANING AND NORMALISATION (5 Marks)

### A2.1 – Cleaning Rules & Justification
1. **Missing Values (`""`, `"NA"`, `"NaN"`):**
   - **Rule:** If `pm25` is missing for a single isolated hour ($gap = 1$ hour) within the same station and day, apply **forward fill** (previous valid hour's value). If consecutive hours are missing ($gap > 1$) or if all pollutant columns are missing, **drop** the row (or impute with station-level median only when computing non-time-series monthly distributions).
   - **Justification:** Air quality exhibits strong short-term autocorrelation over 1 hour, making forward fill accurate for single dropouts without distorting daily averages; multi-hour gaps cannot be reliably guessed and must be excluded.
2. **Impossible Values:**
   - **Rule:** Reject/drop any reading where `pm25 < 0` or `pm25 > 999`, `pm10 < 0` or `pm10 > 1500`, `no2 < 0` or `no2 > 500`, or `temp_c < -5` or `temp_c > 55`.
   - **Justification:** Physical concentrations cannot be negative, and values like `9999` represent sensor error codes (`0xFFFF`/overflow) that would severely skew arithmetic means.
3. **Duplicate Rows:**
   - **Rule:** Deduplicate on the composite key `(station_name, obs_date, obs_hour)` by retaining the first valid record and discarding subsequent duplicates.
   - **Justification:** Counting the same hourly measurement twice gives that hour double weight in daily and monthly averages.
4. **Fahrenheit Temperatures:**
   - **Rule:** For the two stations reporting in Fahrenheit (or whenever `temperature > 55.0`), convert using $T_C = (T_F - 32) \times \frac{5}{9}$.
   - **Justification:** Ensures all stations share a unified Celsius scale ($^\circ C$) before cross-station comparisons or temperature-pollution correlation analysis.

#### Pseudocode – Cleaning Pipeline
```text
ALGORITHM CleanAirQualityRecords(RawRows, FahrenheitStations)
INPUT:  RawRows (list of raw dictionary records), FahrenheitStations (set of station names)
OUTPUT: CleanRows (list of validated, standardised tuples)

BEGIN
    SeenKeys <- empty set
    LastValidPM25 <- empty dictionary
    CleanRows <- empty list

    FOR EACH row IN RawRows DO
        station <- TRIM_AND_TITLE_CASE(row.station_name)
        dateStr <- STANDARDISE_DATE_ISO(row.date)
        hour <- PARSE_INTEGER(row.hour)

        IF station IS EMPTY OR dateStr IS INVALID OR hour < 0 OR hour > 23 THEN
            CONTINUE
        ENDIF

        key <- (station, dateStr, hour)
        IF key IN SeenKeys THEN
            CONTINUE
        ENDIF

        pm25 <- PARSE_FLOAT_OR_NULL(row.pm25)
        IF pm25 IS NULL THEN
            IF (station, dateStr) IN LastValidPM25 THEN
                pm25 <- LastValidPM25[(station, dateStr)]
            ELSE
                CONTINUE
            ENDIF
        ENDIF

        IF pm25 < 0.0 OR pm25 > 999.0 THEN
            CONTINUE
        ENDIF

        pm10 <- PARSE_FLOAT_OR_NULL(row.pm10)
        no2  <- PARSE_FLOAT_OR_NULL(row.no2)
        temp <- PARSE_FLOAT_OR_NULL(row.temperature)

        IF pm10 IS NULL OR pm10 < 0.0 OR pm10 > 1500.0 THEN CONTINUE ENDIF
        IF no2 IS NULL OR no2 < 0.0 OR no2 > 500.0 THEN CONTINUE ENDIF
        IF temp IS NULL THEN CONTINUE ENDIF

        IF station IN FahrenheitStations OR temp > 55.0 THEN
            temp <- (temp - 32.0) * (5.0 / 9.0)
        ENDIF

        IF temp < -5.0 OR temp > 55.0 THEN
            CONTINUE
        ENDIF

        ADD key TO SeenKeys
        LastValidPM25[(station, dateStr)] <- pm25
        APPEND (station, dateStr, hour, ROUND(pm25, 2), ROUND(pm10, 2), ROUND(no2, 2), ROUND(temp, 2)) TO CleanRows
    ENDFOR

    RETURN CleanRows
END
```

### A2.2 – Normalisation Design
1. **Min–Max Normalisation:**
   $$x_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
   - **When Appropriate:** Maps all PM2.5 readings strictly into $[0, 1]$. Best used for **visualisation overlays** (comparing PM2.5, NO2, and Temperature on a single y-axis) and **bounded distance-based ML algorithms** (e.g., k-NN or neural network inputs) when extreme outliers have already been removed.
2. **Z-Score Standardisation:**
   $$z = \frac{x - \mu}{\sigma}$$
   - **When Appropriate:** Centres data at mean $\mu = 0$ with standard deviation $\sigma = 1$. Best used for **anomaly/spike detection** (flagging pollution episodes where $|z| > 3$) and comparing stations with different baseline variances without compressing normal values when an extreme pollution spike occurs.

### A2.3 – Standard Formatting Rules
- **Dates:** ISO-8601 format `YYYY-MM-DD` (e.g., `2026-10-05`), enabling lexicographical sorting and string-prefix filtering (`LIKE '2026-10-%'`).
- **Hours:** Zero-padded or integer 24-hour clock `0` to `23`.
- **Station Names:** Stripped of leading/trailing spaces and formatted in Title Case without underscores (e.g., `"Adyar"`, `"Anna Nagar"`, `"Guindy"`).
- **Numbers:** Standard IEEE 754 `float` rounded to **2 decimal places** for physical measurements (`48.25`) and **3 decimal places** for normalised scores (`0.644`).

### Alternative Concept & Complexity Analysis (Dropping Missing Readings vs Forward Fill / Median Imputation)
- **Alternative Approach:** Immediately drop any row containing a missing value instead of forward-filling or computing a median.
- **Effect on Daily Averages:** If missingness occurs randomly across the day (MCAR), dropping rows leaves the daily mean unbiased (though slightly higher variance due to smaller sample size $k < 24$). However, if sensor dropouts happen systematically during peak afternoon heat or rush-hour traffic (MNAR), dropping missing rows artificially lowers the calculated daily mean.
- **Time & Space Complexity:**
  - **Dropping Missing Rows:** Single linear scan -> **$O(n)$ time**, **$O(1)$ auxiliary space**.
  - **Forward Fill:** Single linear scan tracking one previous value per station -> **$O(n)$ time**, **$O(S)$ auxiliary space** (where $S = 12$ stations, effectively $O(1)$).
  - **Median Imputation:** Sorting $n$ values to find the middle element requires **$O(n \log n)$ time** (or $O(n)$ expected time via Quickselect) and **$O(n)$ auxiliary space** to hold non-null values in memory.

---

## TASK A3 – DESIGN THE ANALYSIS AND VISUALISATION (5 Marks)

### A3.1 – Chart Selection & Justification
1. **Trend of PM2.5 over a month $\rightarrow$ Line Chart:**
   - **Justification:** Time (`obs_date`) is continuous and ordered along the x-axis. Connecting daily mean PM2.5 points with a line clearly reveals temporal trajectories, multi-day smog buildup, and weekend vs weekday dips.
2. **Comparison of stations $\rightarrow$ Bar Chart (or Grouped Bar Chart):**
   - **Justification:** Station names are discrete nominal categories. Bar lengths anchored at a zero baseline allow accurate visual comparison of mean PM2.5 across the 12 stations.
3. **Relationship between temperature and PM2.5 $\rightarrow$ Scatter Plot:**
   - **Justification:** Both variables are continuous numerical measurements. Plotting paired $(T_C, \text{PM2.5})$ observations reveals linear/non-linear correlations, thermal inversion clusters, and outliers.
4. **Hours with the worst air $\rightarrow$ Box Plot (grouped by Hour 0–23):**
   - **Justification:** Each hour of the day has 30+ daily observations across a month. A box plot displays the median, interquartile range (IQR), and extreme pollution spikes for every hour simultaneously, identifying morning/evening rush-hour peaks far better than single averages.

### A3.2 – Daily Summary Table Design
- **Schema (`daily_summary` table / view):**
  `station_name (TEXT), obs_date (TEXT), min_pm25 (REAL), max_pm25 (REAL), mean_pm25 (REAL), valid_readings (INTEGER)`
- **Production Method:** Generated directly in SQLite via an aggregate query:
  ```sql
  SELECT s.station_name, r.obs_date,
         ROUND(MIN(r.pm25), 2) AS min_pm25,
         ROUND(MAX(r.pm25), 2) AS max_pm25,
         ROUND(AVG(r.pm25), 2) AS mean_pm25,
         COUNT(r.pm25) AS valid_readings
  FROM readings r
  JOIN stations s ON r.station_id = s.station_id
  GROUP BY s.station_name, r.obs_date;
  ```

### Alternative Concept & Complexity Analysis (Python Loops vs SQL `GROUP BY`)
- **Alternative Approach:** Fetch all $n$ rows from SQLite/CSV into Python and group them manually into a dictionary `groups[(station, date)].append(pm25)`, then iterate over each group to compute `min()`, `max()`, `sum()/len()`, and `len()`.
- **Time Complexity:** Both SQL `GROUP BY` (using hash aggregation or B-tree index scan) and Python dictionary grouping run in **$O(n)$ average time** across $n$ readings (or $O(n \log n)$ if sort-based grouping is used). However, SQLite executes inside compiled C loops without Python bytecode dispatch or object boxing overhead, making it significantly faster in wall-clock time.
- **Memory Complexity:**
  - **Python Dictionary of Lists:** Stores every individual float inside Python list objects -> **$O(n)$ memory** (high overhead: ~28 bytes per Python `float` plus list pointers).
  - **SQL `GROUP BY`:** Maintains only running accumulators (`min`, `max`, `sum`, `count`) per `(station, date)` group -> **$O(G)$ memory**, where $G = \text{stations} \times \text{days} \ll n$.

---

## TASK A4 – PLAN DEBUGGING AND PROFILING (4 Marks)

### A4.1 – Debugging Plan
1. **`print()` Statements:** Used strictly during initial exploratory prototyping on small 10-row samples to inspect raw CSV dictionary keys and intermediate type conversions.
2. **`assert` Statements:** Embedded as post-condition invariants inside the cleaning pipeline (e.g., `assert 0.0 <= pm25 <= 999.0`, `assert len(date_str) == 10`) to fail fast immediately if corrupted data slips past a filter.
3. **`logging` Module:** Configured with severity levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`) writing to `pipeline.log`. Malformed rows, Fahrenheit conversions, and duplicate skips are logged at `WARNING` level with line numbers without cluttering standard output.
4. **`pdb` / IDE Debugger:** Used (`breakpoint()` or `python -m pdb`) when an `AssertionError` or edge-case parsing bug occurs, allowing step-by-step variable inspection (`p row`, `n`, `c`) at the exact failing record.

### A4.2 – Profiling Plan
1. **`time.perf_counter()`:** Used for coarse macro-benchmarking—measuring total wall-clock elapsed time of end-to-end stages (Acquire, Clean, Insert, Query).
2. **`timeit`:** Used for micro-benchmarking small isolated functions (e.g., comparing regex date parsing vs string slicing over 10,000 iterations) with garbage collection disabled for fair comparison.
3. **`cProfile` (with `pstats`):** Used on full-scale runs (120 stations, ~1M rows) to generate a complete call graph sorted by `tottime` and `cumtime`, pinpointing exact functions (such as `csv.DictReader`, `statistics.mean`, or `sqlite3` commits) consuming the most CPU cycles.

### Alternative Concept & Complexity Analysis (`print()` Everywhere vs `logging` + Debugger)
- **Alternative Approach:** Use `print()` statements across every loop iteration for all debugging instead of `logging` and `pdb`.
- **Performance Overhead:** Every `print()` triggers synchronous I/O system calls (`write()` to stdout/console buffer) and string formatting. Across $n = 1,000,000$ rows, thousands of `print()` calls add $O(n)$ I/O latency, often slowing a 1-second script down to 15–30 seconds.
- **Switching Off in Production:**
  - **`print()`:** Must be manually deleted or commented out across every file, risking accidental removal of legitimate output or leftover debug clutter.
  - **`logging`:** Switched off globally in one line by raising the threshold level (`logging.getLogger().setLevel(logging.ERROR)`), where disabled log calls incur near-zero overhead.

---

## TASK A5 – DESIGN AN AI APPLICATION FOR CITIZEN COMPLAINTS (4 Marks)

### A5.1 – Lexicon Sentiment Scorer & Extractive Summariser
1. **Negation-Aware Lexicon Sentiment Scorer:**
   - Maintain curated sets `POSITIVE`, `NEGATIVE`, and `NEGATORS = {"not", "never", "no"}`.
   - Tokenise text into lowercase words stripped of punctuation. Iterate through tokens: assign `+1` if in `POSITIVE`, `-1` if in `NEGATIVE`, else `0`. If the immediately preceding token (`words[i-1]`) is in `NEGATORS`, multiply the polarity by `-1`. Classify total score $> 0$ as `positive`, $< 0$ as `negative`, else `neutral`.
2. **Frequency-Based Extractive Summariser:**
   - Split complaint text into sentences. Tokenise words, remove common English stopwords (`the`, `is`, `and`, `to`, `in`, etc.), and compute term frequency `freq[word]`.
   - Score each sentence by summing `freq[word]` for its non-stopword tokens (normalised by sentence length to avoid favouring overly long run-on sentences). Select the top-$k$ highest-scoring sentences in their original order.

#### Pseudocode – Sentiment Scorer & Extractive Summariser
```text
ALGORITHM ScoreSentimentWithNegation(Text, PosSet, NegSet, NegatorSet)
INPUT:  Text (string), PosSet, NegSet, NegatorSet (sets of lowercase strings)
OUTPUT: Score (integer), Label (string)

BEGIN
    CleanText <- REMOVE_PUNCTUATION(LOWERCASE(Text))
    Words <- SPLIT_BY_WHITESPACE(CleanText)
    Score <- 0

    FOR i <- 0 TO LENGTH(Words) - 1 DO
        word <- Words[i]
        val <- 0
        IF word IN PosSet THEN
            val <- 1
        ELSE IF word IN NegSet THEN
            val <- -1
        ENDIF

        IF val != 0 AND i > 0 AND Words[i - 1] IN NegatorSet THEN
            val <- -val
        ENDIF

        Score <- Score + val
    ENDFOR

    IF Score > 0 THEN
        Label <- "positive"
    ELSE IF Score < 0 THEN
        Label <- "negative"
    ELSE
        Label <- "neutral"
    ENDIF

    RETURN Score, Label
END
```

### A5.2 – Rule-Based Chatbot Design & Limitations
- **Design:**
  1. Convert user query to lowercase and match against known station names (`Adyar`, `Guindy`, etc.) and pollutant keywords (`pm2.5`, `pm10`, `no2`, `temperature`).
  2. Extract temporal keywords (`today`, `latest`, `average`, `october`).
  3. Map matched intent to a safe **parameterised SQL query** (`SELECT pm25, obs_date, obs_hour FROM readings ... WHERE station_name = ? ORDER BY obs_date DESC, obs_hour DESC LIMIT 1`).
  4. Format the returned database tuple into a human-readable response template.
- **Limitations:**
  1. Fails on spelling mistakes or aliases (e.g., `"Adiar"` or `"IIT area"`).
  2. Cannot handle multi-turn context or follow-up pronouns (`"What about yesterday there?"`).
  3. Rigid templates cannot answer complex comparative or causal questions (`"Why did pollution spike near the highway last night?"`).

### Alternative Concept & Complexity Analysis (Trained ML / Pre-Trained Language Model vs Word List)
- **Alternative Approach:** Replace the word-list scorer with a trained Naive Bayes classifier (TF-IDF + MultinomialNB) or a pre-trained Transformer (e.g., DistilBERT).
- **Time per Complaint:**
  - **Word List:** $O(w)$ hash-set lookups per complaint of $w$ words (~0.02 ms per complaint).
  - **Naive Bayes:** $O(w)$ sparse vector dot-product (~0.1 ms per complaint).
  - **Pre-Trained Transformer:** $O(w^2)$ self-attention matrix multiplications (~15–50 ms on CPU per complaint).
- **Memory Needed:**
  - **Word List:** ~5 KB for Python sets.
  - **Naive Bayes:** ~1–5 MB for vocabulary and log-probability matrices.
  - **Pre-Trained Transformer:** ~250 MB–1.5 GB for model weights in RAM/VRAM.
- **Expected Accuracy:**
  - **Word List:** ~70–82% (struggles with sarcasm, idioms, and unseen words).
  - **Naive Bayes:** ~82–87% when trained on domain-labelled complaints.
  - **Pre-Trained Transformer:** ~90–95% (captures deep contextual semantics and subtle negation).
