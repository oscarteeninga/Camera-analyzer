import sqlite3
import time

DATABASE = "data.db"


def init_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS cameras
                                        (id INTEGER PRIMARY KEY, 
                                        name VARCHAR(50),
                                         ip varchar(50),
                                          username varchar(50), 
                                          password varchar(50))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS areas
                            (id INTEGER PRIMARY KEY,
                             name varchar(1),
                             coverage_required varchar(50),
                             x integer, 
                             y integer,
                             w integer,
                             h integer,
                             camera_id BIGINT,FOREIGN KEY(camera_id) REFERENCES cameras(id))''')


class CamerasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        c = self.conn.cursor()
        init_tables(c)
        self.conn.commit()

    def insert_camera(self, name, ip, username, password):
        c = self.conn.cursor()
        c.execute("INSERT INTO cameras(name,ip, username, password) VALUES (?,?,?,?)",
                  [name, ip, username, password])
        self.conn.commit()
        return c.lastrowid

    def update_camera(self, id, name, ip, username, password):
        c = self.conn.cursor()
        query = "UPDATE cameras SET name = '{0}' , ip = '{1}', username = '{2}', password = '{3}' WHERE id = '{4}'".format(
            name, ip, username, password, id)
        c.execute(query)
        self.conn.commit()

    def delete_camera(self, id):
        c = self.conn.cursor()
        query = "DELETE FROM cameras WHERE ID ='{0}'".format(id)
        c.execute(query)
        self.conn.commit()

    def read_camera(self, id):
        c = self.conn.cursor()
        query = "select * from cameras where id={0}".format(id)
        c.execute(query)
        return c.fetchone()

    def read_cameras(self):
        c = self.conn.cursor()
        query = "select * from cameras"
        c.execute(query)
        return c.fetchall()


class AreasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        c = self.conn.cursor()
        init_tables(c)
        self.conn.commit()

    def get_name(self, camera_id):
        return "ABCDEFGDIJKLMNOP"[len(self.read_areas(camera_id))]

    def insert_area(self, confidence_required, x, y, w, h, camera_id):
        name = self.get_name(camera_id)
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO areas(name, coverage_required, x, y, w, h, camera_id) VALUES (?,?,?,?,?,?,?)",
            [name, confidence_required, x, y, w, h, camera_id])
        self.conn.commit()
        return c.lastrowid

    def update_area(self, id, coverage_required, x, y, w, h):
        c = self.conn.cursor()
        query = f"UPDATE areas SET coverage_required = '{coverage_required}', x = '{x}', y = '{y}', w = '{w}', h = '{h}' WHERE id= '{id}'"
        c.execute(query)
        self.conn.commit()

    def read_areas(self, camera_id=None):
        c = self.conn.cursor()
        query = 'select * from areas'
        if camera_id:
            query += f" where camera_id = '{camera_id}'"
        query += ' order by id'
        c.execute(query)
        return c.fetchall()

    def read_area(self, id):
        c = self.conn.cursor()
        query = "select * from areas where id = '{0}'".format(id)
        c.execute(query)
        return c.fetchone()

    def delete_area(self, id):
        # tu jest fuszerka, ale nie miałem lepszego pomysłu
        area = self.read_area(id)
        if area:
            camera_id = str(area[-1])
            camera_areas = self.read_areas(camera_id)
            self.delete_area_for_camera(camera_id)
            for area in camera_areas:
                if str(area[0]) != str(id):
                    self.insert_area(area[2], area[3], area[4], area[5], area[6], area[7])
            self.conn.commit()

    def delete_area_for_camera(self, camera_id):
        c = self.conn.cursor()
        query = f"DELETE FROM areas WHERE camera_id = '{camera_id}'"
        c.execute(query)
        self.conn.commit()


class EventsRepository:
    def __init__(self, data_base):
        self.events = []
        self.max_id = 0

    def insert_event(self, type, confidence, area_name, camera_name):
        timestamp = int(time.time() * 1000)
        self.clear_old_events(timestamp)
        event = Event(self.max_id + 1, timestamp, type, confidence, area_name, camera_name)
        self.max_id = self.max_id + 1
        self.events.append(event)
        return self.max_id

    def read_events(self, date_from=None):
        if date_from is not None:
            timestamp = int(date_from)
            events = list(filter(lambda e: e.timestamp >= timestamp, self.events))
        else:
            events = self.events
        return events

    def clear_old_events(self, timestamp):
        # remove events older than 5 seconds from now
        self.events = list(filter(lambda event: event.timestamp + 5000 > timestamp, self.events))


class Event:
    def __init__(self, id, timestamp, type, confidence, area_name, camera_name):
        self.id = id
        self.timestamp = timestamp
        self.type = type
        self.confidence = confidence
        self.area_name = area_name
        self.camera_name = camera_name
