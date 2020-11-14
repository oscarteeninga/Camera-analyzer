import time

import cv2


class CameraConfig:

    @staticmethod
    def from_list(l):
        return CameraConfig(l[1], l[2], l[3], l[4])

    def __init__(self, name, ip, username, password):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password

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
