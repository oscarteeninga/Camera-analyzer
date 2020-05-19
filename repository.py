import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS events
             (date datetime, object varchar(255))''')

conn.commit()


def insert(objectname):
    c = conn.cursor()
    c.execute("INSERT INTO events(date,object) VALUES (current_timestamp ,?)", [objectname])
    conn.commit()


def read():
    cur = conn.cursor()
    cur.execute("select object,date from events")
    return cur.fetchall()
