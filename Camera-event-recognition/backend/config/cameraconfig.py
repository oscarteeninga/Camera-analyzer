import cv2


class CameraConfig:

    @staticmethod
    def from_list(l):
        return CameraConfig(l[0], l[1], l[2], l[3], l[4], l[5])

    def __init__(self, id, name, ip, username, password, fit_video_to_areas):
        self.id = id
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.fit_video_to_areas = fit_video_to_areas

    def to_json(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'name': self.name,
            'user': self.username,
            'password': self.password,
            'fit_video_to_areas': self.fit_video_to_areas
        }

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def capture(self):
        return cv2.VideoCapture('rtsp://' + self.username + ':' + self.password + '@' + self.ip + ':554')
