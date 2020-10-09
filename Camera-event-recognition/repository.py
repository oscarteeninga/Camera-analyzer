import sqlite3


class Repository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS events
                     (date datetime, confidence varchar(50), object varchar(50), 
                     x integer, y integer, w integer, h integer)''')
        self.conn.commit()

    def insert(self, objectname, confidence, x, y, w, h):
        print("Saving event: " + objectname + " with confidence: " + str(confidence))
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO events(date,object,confidence, x, y, w, h) VALUES (current_timestamp ,?,?,?,?,?,?)",
                  [objectname, confidence, x, y, w, h])
        self.conn.commit()

    def read(self):
        cur = self.conn.cursor()
        cur.execute("select object,date,confidence from events")
        return cur.fetchall()
