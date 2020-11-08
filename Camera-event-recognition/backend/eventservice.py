import json

from areaservice import AreaService
from model.repository import Repository

DATABASE = "events"
area_service = AreaService()


class EventService:
    def __init__(self):
        self.repository = Repository(DATABASE)

    def get_events(self, date_from):
        database_events = self.repository.read_events(date_from)
        # self.repository.insert_into_events("human", 1, 10,10,10,10)
        # self.repository.insert_into_events("human", 1, 10, 10, 5, 5)
        # self.repository.insert_into_events("human", 1, 10, 10, 20, 20)
        # self.repository.insert_into_events("human", 1, 10, 10, 10, 200)
        return self.parse_events(database_events)

    def parse_events(self, events):
        jsons = []
        for event in events:
            dic = {
                "type": event[2],
                "confidence": event[1],
                "device": "192.168.1.110",
                "timestamp": event[0],
                "area": area_service.recognize_area(event[3], event[4], event[5], event[6])
            }
            jsons.append(dic)
        return json.dumps(jsons)
