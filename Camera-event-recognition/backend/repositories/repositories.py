import sqlite3
import time

DATABASE = "data.db"


def init_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS cameras
                                        (id VARCHAR(50) PRIMARY KEY, ip varchar(50), username varchar(50), password varchar(50))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS areas
                             (name varchar(1), confidence_required varchar(50),
                             x integer, y integer, w integer, h integer, camera_id BIGINT,FOREIGN KEY(camera_id) REFERENCES cameras(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                        (id INTEGER PRIMARY KEY,date bigint, confidence varchar(50), object varchar(50), 
                        x integer, y integer, w integer, h integer, camera_id VARCHAR(50),  FOREIGN KEY(camera_id) REFERENCES cameras(id))''')


class CamerasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        init_tables(self.c)
        self.conn.commit()

    def insert_camera(self, id, ip, username, password):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO cameras(id, ip, username, password) VALUES (?,?,?,?)",
                       [id, ip, username, password])
        self.conn.commit()
        return self.c.lastrowid

    def update_camera(self, id, ip, username, password):
        self.c = self.conn.cursor()
        self.delete_camera(id)
        self.insert_camera(id, ip, username, password)
        self.conn.commit()

    def delete_camera(self, id):
        self.c = self.conn.cursor()
        query = "DELETE FROM cameras WHERE ID ='{0}'".format(id)
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

    def update_area(self, new_name, confidence_required, x, y, w, h, camera_id, name):
        self.c = self.conn.cursor()
        query = f"UPDATE areas SET name = '{new_name}', confidence_required = '{confidence_required}', x = '{x}', y = '{y}', w = '{w}', h = '{h}' WHERE camera_id = '{camera_id}' and name = '{name}'"
        self.c.execute(query)
        self.conn.commit()

    def read_areas(self, id):
        cur = self.conn.cursor()
        query = 'select * from areas'
        if id is not None:
            query += " where camera_id = '{0}'".format(id)
        cur.execute(query)
        values = cur.fetchall()
        return values

    def read_area(self, name):
        cur = self.conn.cursor()
        query = 'select * from areas'
        if name is not None:
            query += " and name = '{0}'".format(name)
        cur.execute(query)
        values = cur.fetchall()
        return values

    def delete_area(self, id, name):
        self.c = self.conn.cursor()
        query = f"DELETE FROM areas WHERE camera_id ='{id}' and name='{name}'"
        self.c.execute(query)
        self.conn.commit()


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
