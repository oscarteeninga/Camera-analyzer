import queue, threading
from config.cameraconfig import CameraConfig


class Receiver:
    def __init__(self, camera_config: CameraConfig):
        self.cap = camera_config.capture()
        self.q = queue.Queue()
        self.on = True
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def stop(self):
        self.cap.release()
        self.on = False

    def _reader(self):
        while self.on:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()
