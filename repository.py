import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS events
             (date datetime, confidence varchar(50), object varchar(50))''')

conn.commit()


def insert(objectname, confidence):
    c = conn.cursor()
    c.execute("INSERT INTO events(date,object,confidence) VALUES (current_timestamp ,?,?)",
              [objectname, confidence])
    conn.commit()


def read():
    cur = conn.cursor()
    cur.execute("select object,date,confidence from events")
    return cur.fetchall()
