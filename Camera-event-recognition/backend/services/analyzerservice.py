import threading
import cv2
import sys
import os


sys.path.append(os.path.join("backend"))
from model.analyzer import Analyzer


class AnalyzerService:
    def __init__(self, event_service, camera_service, area_service):
        self.analyzers = {}
        self.camera_service = camera_service
        self.area_service = area_service
        self.event_service = event_service

    def add(self, analyzer: Analyzer, camera_name):
        self.analyzers[camera_name] = analyzer

    def start(self, id):
        conf = self.camera_service.get_config(id)
        if conf is None or conf in self.analyzers.keys():
            return False
        else:
            analyzer = Analyzer(self.event_service, self.area_service, conf)
            thread = threading.Thread(target=analyzer.video)
            thread.start()
            self.analyzers[conf] = analyzer
            return True

    def start_all(self):
        for conf in self.camera_service.get_configs():
            analyzer = Analyzer(self.event_service, self.area_service, conf)
            thread = threading.Thread(target=analyzer.video)
            thread.start()
            self.analyzers[conf] = analyzer
        return True

    def stop_all(self):
        for analyzer in self.analyzers.values():
            analyzer.stop()
        self.analyzers.clear()
        return True

    def stop(self, id):
        conf = self.camera_service.get_config(id)
        if conf is None or conf not in self.analyzers.keys():
            return False
        else:
            self.analyzers[conf].stop()
            self.analyzers.pop(conf)
            return True

    def state_response(self, conf):
        if conf is None:
            return "not exists"
        elif conf in self.analyzers.keys():
            return "on"
        else:
            return "off"

    def state_all(self):
        states = {}
        for conf in self.camera_service.get_configs():
            states[conf.id] = self.state_response(conf)
        return states

    def state(self, id):
        return self.state_response(self.camera_service.get_config(id))

    def get_video(self, id):
        conf = self.camera_service.get_config(id)
        if conf:
            if conf in self.analyzers.keys():
                analyzer = self.analyzers.get(conf)
                sender = analyzer.sender
                while True:
                    image = sender.get()
                    if image is None:
                        break
                    else:
                        (flag, encodedImage) = cv2.imencode(".jpg", image)
                        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
            else:
                yield "Cannot connect to device for config " + str(conf)
        else:
            yield "Device config does not exist"



