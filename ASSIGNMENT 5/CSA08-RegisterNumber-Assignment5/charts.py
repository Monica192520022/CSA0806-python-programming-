# charts.py - the four charts of Task A3.1 / B1.4
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

con = sqlite3.connect("airquality.db")

# 1. Line chart: daily mean PM2.5 of every station over the month
plt.figure(figsize=(8, 4))
for name in ["Adyar", "Guindy", "Velachery", "Perungudi"]:
    q = """SELECT r.day, AVG(r.pm25) FROM readings r JOIN stations s ON r.station_id = s.station_id
           WHERE s.name = ? GROUP BY r.day ORDER BY r.day"""
    data = con.execute(q, (name,)).fetchall()
    plt.plot([int(d[0][-2:]) for d in data], [d[1] for d in data], label=name)
plt.xlabel("Day of October 2026")
plt.ylabel("Daily mean PM2.5 (ug/m3)")
plt.title("Trend of PM2.5 over October")
plt.legend()
plt.savefig("charts/1_line_trend.png", dpi=100, bbox_inches="tight")

# 2. Bar chart: station comparison
q = """SELECT s.name, AVG(r.pm25) FROM readings r JOIN stations s ON r.station_id = s.station_id
       GROUP BY s.name ORDER BY s.name"""
data = con.execute(q).fetchall()
plt.figure(figsize=(6, 4))
plt.bar([d[0] for d in data], [d[1] for d in data])
plt.xlabel("Station")
plt.ylabel("Mean PM2.5 (ug/m3)")
plt.title("Mean PM2.5 by station")
plt.savefig("charts/2_bar_stations.png", dpi=100, bbox_inches="tight")

# 3. Scatter plot: temperature against PM2.5
data = con.execute("SELECT temp_c, pm25 FROM readings WHERE temp_c IS NOT NULL").fetchall()
x = [d[0] for d in data]
y = [d[1] for d in data]
plt.figure(figsize=(6, 4))
plt.scatter(x, y, s=4, alpha=0.4)
plt.xlabel("Temperature (C)")
plt.ylabel("PM2.5 (ug/m3)")
plt.title("Temperature and PM2.5")
plt.savefig("charts/3_scatter_temp_pm25.png", dpi=100, bbox_inches="tight")
n = len(x)
mx, my = sum(x) / n, sum(y) / n
cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
corr = cov / (sum((a - mx) ** 2 for a in x) ** 0.5 * sum((b - my) ** 2 for b in y) ** 0.5)
print("Correlation between temperature and PM2.5:", round(corr, 3))

# 4. Bar chart of the average PM2.5 for each hour (hours with the worst air)
data = con.execute("SELECT hour, AVG(pm25) FROM readings GROUP BY hour ORDER BY hour").fetchall()
plt.figure(figsize=(8, 4))
plt.bar([d[0] for d in data], [d[1] for d in data])
plt.xlabel("Hour of the day")
plt.ylabel("Mean PM2.5 (ug/m3)")
plt.title("Average PM2.5 for each hour")
plt.savefig("charts/4_bar_hours.png", dpi=100, bbox_inches="tight")

# 5. Histogram and box plot of PM2.5
values = [d[0] for d in con.execute("SELECT pm25 FROM readings")]
plt.figure(figsize=(6, 4))
plt.hist(values, bins=30)
plt.xlabel("PM2.5 (ug/m3)")
plt.ylabel("Number of readings")
plt.title("Distribution of PM2.5")
plt.savefig("charts/5_histogram.png", dpi=100, bbox_inches="tight")

plt.figure(figsize=(6, 4))
groups = []
names = ["Adyar", "Guindy", "Velachery", "Perungudi"]
for name in names:
    q = """SELECT r.pm25 FROM readings r JOIN stations s ON r.station_id = s.station_id WHERE s.name = ?"""
    groups.append([d[0] for d in con.execute(q, (name,))])
plt.boxplot(groups, tick_labels=names)
plt.ylabel("PM2.5 (ug/m3)")
plt.title("PM2.5 spread of each station")
plt.savefig("charts/6_boxplot.png", dpi=100, bbox_inches="tight")

# first and last week means for the trend interpretation
a = con.execute("SELECT AVG(pm25) FROM readings WHERE day <= '2026-10-07'").fetchone()[0]
b = con.execute("SELECT AVG(pm25) FROM readings WHERE day >= '2026-10-25'").fetchone()[0]
print("Mean PM2.5 first week:", round(a, 1), "| last week:", round(b, 1))
con.close()
