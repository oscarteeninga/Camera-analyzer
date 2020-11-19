import threading

import numpy as np
from PIL import Image
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
            thread = threading.Thread(target=analyzer.video, args=(True,))
            # thread.start()
            self.analyzers[conf] = analyzer
            return True

    def start_all(self):
        for conf in self.camera_service.get_configs():
            analyzer = Analyzer(self.event_service, self.area_service, conf)
            thread = threading.Thread(target=analyzer.video, args=(True,))
            # thread.start()
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

    def image(self, id):
        conf = self.camera_service.get_config(id)
        if conf is None or conf not in self.analyzers.keys():
            return None
        else:
            analyzer = self.analyzers[conf]
            return Image.fromarray(np.array(analyzer.capture.read()))

