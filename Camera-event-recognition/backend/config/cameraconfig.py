import time

import cv2


class CameraConfig:

    @classmethod
    def from_list(cls, l, api=False):
        print(l)
        return CameraConfig(l[1], l[2], l[3], l[4], l[5], api=api)

    def __init__(self, name, ip, username, password, fps=None, api=False):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        if fps and fps > 0:
            self.fps = fps
        else:
            self.fps = self.check_fps()

    def __str__(self):
        return self.ip + "," + self.username + "," + self.password

    def serialize(self):
        return {
            'name': self.name,
            'ip': self.ip,
            'username': self.username,
            'password': self.password
        }

    def capture(self):
        return cv2.VideoCapture('rtsp://' + self.username + ':' + self.password + '@' + self.ip + ':554')

    def check_fps(self):
        c = self.capture()
        b = time.time()
        for _ in range(150):
            c.read()
        return int(150 / (time.time() - b))
