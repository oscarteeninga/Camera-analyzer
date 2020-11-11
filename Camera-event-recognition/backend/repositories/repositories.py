import sqlite3
import time

DATABASE = "db"


class CamerasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS cameras
                                     (id INTEGER, name varchar(50), ip varchar(50), username varchar(50), password varchar(50), fps integer,  PRIMARY KEY(id))''')
        self.conn.commit()

    def insert_camera(self, name, ip, username, password, fps):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO cameras(name, ip, username, password, fps) VALUES (?,?,?,?,?)",
                           [name, ip, username, password, fps])
        self.conn.commit()

    def read_camera(self, id):
        cur = self.conn.cursor()
        query = "select * from cameras where id = " + str(id)
        cur.execute(query)

        return cur.fetchone()

    def read_cameras(self):
        cur = self.conn.cursor()
        cur.execute("select * from cameras")
        return cur.fetchall()


class AreasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS areas
                             (name varchar(1), confidence_required varchar(50),
                             x integer, y integer, w integer, h integer, camera_id INTEGER, FOREIGN KEY(camera_id) REFERENCES camera(id))''')
        self.conn.commit()

    def insert_area(self, name, confidence_required, x, y, w, h):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO areas(name, confidence_required, x, y, w, h) VALUES (?,?,?,?,?,?)",
                       [name, confidence_required, x, y, w, h])
        self.conn.commit()

    def read_areas(self):
        cur = self.conn.cursor()
        cur.execute("select * from areas")
        values = cur.fetchall()
        return values


class EventsRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS events
                     (date bigint, confidence varchar(50), object varchar(50), 
                     x integer, y integer, w integer, h integer, camera_id INTEGER,  FOREIGN KEY(camera_id) REFERENCES camera(id))''')
        self.conn.commit()

    def insert_event(self, objectname, confidence, x, y, w, h, camera_id):
        print("Saving event: " + objectname + " with confidence: " + str(confidence))
        self.c = self.conn.cursor()
        timestamp = time.time() * 1000
        self.c.execute(
            "INSERT INTO events(date,object,confidence, x, y, w, h,camera_id) VALUES (?,?,?,?,?,?,?,?)",
            [timestamp, objectname, confidence, x, y, w, h, camera_id])
        self.conn.commit()

    def read_events(self, date_from=None):
        cur = self.conn.cursor()
        query = "select * from events"
        if date_from is not None:
            query += " where date > " + date_from
        cur.execute(query)
        values = cur.fetchall()
        return values
