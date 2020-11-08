import sqlite3


class Repository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS events
                     (date datetime, confidence varchar(50), object varchar(50), 
                     x integer, y integer, w integer, h integer, camera_id INTEGER,  FOREIGN KEY(camera_id) REFERENCES camera(id))''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS areas
                             (name varchar(1), confidence_required varchar(50),
                             x integer, y integer, w integer, h integer, camera_id INTEGER, FOREIGN KEY(camera_id) REFERENCES camera(id))''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS cameras
                                     (id INTEGER ,name varchar(50), ip varchar(50), password varchar(50), fps integer,  PRIMARY KEY(id))''')
        self.conn.commit()

    def insert_into_events(self, objectname, confidence, x, y, w, h):
        print("Saving event: " + objectname + " with confidence: " + str(confidence))
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO events(date,object,confidence, x, y, w, h) VALUES (current_timestamp ,?,?,?,?,?,?)",
                       [objectname, confidence, x, y, w, h])
        self.conn.commit()

    def read_events(self, date_from):
        cur = self.conn.cursor()
        query = "select * from events"
        if date_from is not None:
            query += " where date > " + date_from
        cur.execute(query)
        values = cur.fetchall()
        return values

    def insert_into_areas(self, name, confidence_required, x, y, w, h):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO areas(name, confidence_required, x, y, w, h) VALUES (?,?,?,?,?,?)",
                       [name, confidence_required, x, y, w, h])
        self.conn.commit()

    def read_areas(self):
        cur = self.conn.cursor()
        cur.execute("select * from areas")
        values = cur.fetchall()
        return values

    def read_camera_name(self, id):
        cur = self.conn.cursor()
        query = "select name from cameras where id = " + str(id)
        cur.execute(query)
        values = cur.fetchone()

        return values[0]

