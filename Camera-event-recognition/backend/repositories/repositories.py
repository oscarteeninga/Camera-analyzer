import sqlite3
import time

DATABASE = "data.db"


def init_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS cameras
                                        (ID INTEGER PRIMARY KEY, name varchar(50), ip varchar(50), username varchar(50), password varchar(50))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS areas
                             (name varchar(1), confidence_required varchar(50),
                             x integer, y integer, w integer, h integer, camera_id BIGINT,FOREIGN KEY(camera_id) REFERENCES cameras(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                        (id INTEGER PRIMARY KEY,date bigint, confidence varchar(50), object varchar(50), 
                        x integer, y integer, w integer, h integer, camera_id BIGINT,  FOREIGN KEY(camera_id) REFERENCES cameras(id))''')


class CamerasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        init_tables(self.c)
        self.conn.commit()

    def insert_camera(self, name, ip, username, password):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO cameras(name, ip, username, password) VALUES (?,?,?,?)",
                       [name, ip, username, password])
        self.conn.commit()

    def update_camera(self, id, name, ip, username, password):
        self.c = self.conn.cursor()
        query = "UPDATE cameras SET name = '{0}' , ip = '{1}', username = '{2}', password = '{3}' WHERE id = '{4}'".format(
            name, ip, username, password, id)
        self.c.execute(query)
        self.conn.commit()

    def read_camera(self, id):
        cur = self.conn.cursor()
        query = "select * from cameras where cameras.id= '%s'" % id
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
        init_tables(self.c)
        self.conn.commit()

    def insert_area(self, name, confidence_required, x, y, w, h, camera_id):
        self.c = self.conn.cursor()
        self.c.execute(
            "INSERT INTO areas(name, confidence_required, x, y, w, h, camera_id) VALUES (?,?,?,?,?,?,?)",
            [name, confidence_required, x, y, w, h, camera_id])
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
        init_tables(self.c)
        self.conn.commit()

    def insert_event(self, objectname, confidence, x, y, w, h, camera_id):
        self.c = self.conn.cursor()
        timestamp = int(time.time() * 1000)
        self.c.execute(
            "INSERT INTO events(date,object,confidence, x, y, w, h,camera_id) VALUES (?,?,?,?,?,?,?,?)",
            [timestamp, objectname, confidence, x, y, w, h, camera_id])
        self.conn.commit()
        return str(timestamp)

    def read_events(self, page=None, size=None, date_from=None):
        cur = self.conn.cursor()
        if size is None:
            size = 20
        if page is None:
            page = 0
        query = "select * from events"
        if date_from is not None:
            query += " where `date` > %s" % date_from
        limitq = " limit %d,%d" % ((page * size), size)
        query += limitq
        cur.execute(query)
        values = cur.fetchall()
        return values
