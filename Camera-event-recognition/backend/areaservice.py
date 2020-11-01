import json

from model.repository import Repository
from receiver import DetectBox

DATABASE = "areas"


class AreaService:
    def __init__(self):
        self.repository = Repository(DATABASE)

    def get_areas(self):
        database_areas = self.repository.read_areas()
        # self.repository.insert_into_areas("a", 0.7, 10, 10, 10, 10)
        # self.repository.insert_into_areas("b", 0.5, 30, 30, 10, 10)
        return self.parse_areas(database_areas)

    def recognize_area(self, x, y, width, height):
        areas = self.repository.read_areas()
        for area in areas:
            detect_box = DetectBox(area[2], area[3], area[4], area[5])
            if float(area[1]) <= detect_box.coverage(x, y, width, height):
                return area[0]
        return ""

    def parse_areas(self, areas):
        jsons = []
        for area in areas:
            dic = {
                "name": area[0],
                "confidence_required": area[1],
                "x": area[2],
                "y": area[3],
                "width": area[4],
                "height": area[5],
            }
            jsons.append(dic)
        return json.dumps(jsons)
