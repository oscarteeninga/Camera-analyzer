import cv2


class CameraConfig:

    @staticmethod
    def from_list(l):
        return CameraConfig(l[0], l[1], l[2], l[3], l[4])

    def __init__(self, id, name, ip, username, password):
        self.id = id
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'username': self.username,
            'password': self.password
        }

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def capture(self):
        return cv2.VideoCapture('rtsp://' + self.username + ':' + self.password + '@' + self.ip + ':554')
