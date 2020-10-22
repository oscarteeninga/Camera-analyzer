import time
import cv2


class CameraConfig:
    def __init__(self, camera_ip, camera_user, camera_password, fps=None):
        b = time.time()
        self.camera_ip = camera_ip
        self.camera_user = camera_user
        self.camera_password = camera_password
        self.fps = fps

    def __str__(self):
        return self.camera_ip + "," + self.camera_user + "," + self.camera_password

    def fps(self):
        if not self.fps:
            b = time.time()
            for _ in range(150):
                self.capture().read()
            self.fps = int(150 / (time.time() - b))
        return self.fps

    def capture(self):
        return cv2.VideoCapture('rtsp://' + self.camera_user + ':' + self.camera_password + '@' + self.camera_ip + ':554')


