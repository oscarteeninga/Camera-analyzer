import queue

from config.cameraconfig import CameraConfig


class Sender:
    def __init__(self):
        self.queue = queue.Queue(1)

    def put(self, image):
        while not self.queue.empty():
            self.queue.get()
        self.queue.put(image)

    def get(self):
        return self.queue.get()
