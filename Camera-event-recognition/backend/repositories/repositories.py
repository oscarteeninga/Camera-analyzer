import sqlite3

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
                             coverage_required varchar(50),
                             x integer, 
                             y integer,
                             w integer,
                             h integer,
                             camera_id BIGINT,FOREIGN KEY(camera_id) REFERENCES cameras(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                        (id INTEGER PRIMARY KEY,
                        date bigint, 
                        confidence varchar(50),
                        type varchar(50), 
                        camera_name VARCHAR(50),
                        area_name VARCHAR(1))''')


class CamerasRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        init_tables(self.c)
        self.conn.commit()

    def insert_camera(self, name, ip, username, password):
        self.c = self.conn.cursor()
        self.c.execute("INSERT INTO cameras(name,ip, username, password) VALUES (?,?,?,?)",
                       [name, ip, username, password])
        self.conn.commit()
        return self.c.lastrowid

    def update_camera(self, id, name, ip, username, password):
        self.c = self.conn.cursor()
        query = "UPDATE cameras SET name = '{0}' , ip = '{1}', username = '{2}', password = '{3}' WHERE id = '{4}'".format(
            name, ip, username, password, id)
        self.c.execute(query)
        self.conn.commit()

    def delete_camera(self, id):
        self.c = self.conn.cursor()
        query = "DELETE FROM cameras WHERE ID ='{0}'".format(id)
        self.c.execute(query)
        self.conn.commit()

    def read_camera(self, id):
        cur = self.conn.cursor()
        query = "select * from cameras where id={0}".format(id)
        cur.execute(query)

        camera = cur.fetchone()
        return camera

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

    def insert_area(self, confidence_required, x, y, w, h, camera_id):
        self.c = self.conn.cursor()
        self.c.execute(
            "INSERT INTO areas(coverage_required, x, y, w, h, camera_id) VALUES (?,?,?,?,?,?)",
            [confidence_required, x, y, w, h, camera_id])
        self.conn.commit()
        return self.c.lastrowid

    def update_area(self, id, confidence_required, x, y, w, h, camera_id):
        self.c = self.conn.cursor()
        query = f"UPDATE areas SET confidence_required = '{confidence_required}', x = '{x}', y = '{y}', w = '{w}', h = '{h}' WHERE camera_id = '{camera_id}' and id= '{id}'"
        self.c.execute(query)
        self.conn.commit()

    def read_areas(self):
        cur = self.conn.cursor()
        query = 'select * from areas order by id'
        cur.execute(query)
        values = cur.fetchall()
        return values

    def read_area(self, id):
        cur = self.conn.cursor()
        query = "select * from areas where id = '{0}'".format(id)
        cur.execute(query)
        values = cur.fetchall()
        return values

    def delete_area(self, id):
        self.c = self.conn.cursor()
        query = f"DELETE FROM areas WHERE id ='{id}'"
        self.c.execute(query)
        self.conn.commit()


class EventsRepository:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base, check_same_thread=False)
        self.c = self.conn.cursor()
        init_tables(self.c)
        self.conn.commit()

    def insert_event(self, type, timestamp, confidence, area_name, camera_name):
        self.c = self.conn.cursor()
        self.c.execute(
            "INSERT INTO events(date,type,confidence, area_name,camera_name) VALUES (?,?,?,?,?)",
            [timestamp, type, confidence, area_name, camera_name])
        self.conn.commit()
        return self.c.lastrowid

    def read_events(self, page=None, size=None, date_from=None):
        cur = self.conn.cursor()
        if size is None:
            size = 20
        if page is None:
            page = 0
        query = "select id, date,confidence,type, camera_name, area_name from events "
        if date_from is not None:
            query += " where `date` > %s" % date_from
        limitq = " limit %d,%d" % ((page * size), size)
        query += limitq
        cur.execute(query)
        values = cur.fetchall()
        return values
