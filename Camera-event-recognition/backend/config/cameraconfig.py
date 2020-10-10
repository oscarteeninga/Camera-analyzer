import time
import cv2


class CameraConfig:
    def __init__(self, camera_ip, camera_user, camera_password, fps=None):
        self.capture = cv2.VideoCapture('rtsp://' + camera_user + ':' + camera_password + '@' + camera_ip + ':554')
        b = time.time()

        if fps:
            self.fps = fps
        else:
            for _ in range(150):
                self.capture.read()

            self.fps = int(150 / (time.time() - b))
