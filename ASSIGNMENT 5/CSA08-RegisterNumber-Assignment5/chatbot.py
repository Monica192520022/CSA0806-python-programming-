# chatbot.py - rule based chatbot: keywords decide the question, SQLite gives the answer
import sqlite3

STATIONS = ["adyar", "guindy", "velachery", "perungudi"]
con = sqlite3.connect("airquality.db")
TODAY = con.execute("SELECT MAX(day) FROM readings").fetchone()[0]       # latest day in the database


def reply(question):
    q = question.lower()
    station = None
    for s in STATIONS:
        if s in q:
            station = s.title()

    if "pm2.5" in q or "pm25" in q or "air" in q:
        if station is not None:
            row = con.execute("""SELECT ROUND(AVG(r.pm25), 1) FROM readings r JOIN stations s
                                 ON r.station_id = s.station_id WHERE s.name = ? AND r.day = ?""",
                              (station, TODAY)).fetchone()
            if row[0] is None:
                return "Sorry, I have no reading for " + station + " on " + TODAY + "."
            return "The average PM2.5 in " + station + " on " + TODAY + " is " + str(row[0]) + " ug/m3."
        if "worst" in q or "most polluted" in q or "highest" in q:
            row = con.execute("""SELECT s.name, ROUND(AVG(r.pm25), 1) AS a FROM readings r JOIN stations s
                                 ON r.station_id = s.station_id WHERE r.day = ? GROUP BY s.name
                                 ORDER BY a DESC LIMIT 1""", (TODAY,)).fetchone()
            return row[0] + " has the worst air today (PM2.5 " + str(row[1]) + " ug/m3)."
        return "Which station do you mean? I know Adyar, Guindy, Velachery and Perungudi."
    if "hello" in q or "hi" in q.split():
        return "Hello! Ask me about the PM2.5 level of a station."
    return "Sorry, I can only answer questions about PM2.5 and the stations."


for question in ["Hello",
                 "What is the PM2.5 in Adyar today?",
                 "Which station has the worst air today?",
                 "What is the pm2.5 in Chennai?",
                 "Is it safe to go jogging in Guindy?",
                 "What is the PM2.5 in Adyar yesterday?",
                 "Tell me a joke"]:
    print("Q:", question)
    print("A:", reply(question))
