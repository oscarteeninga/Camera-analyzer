from config.areaconfig import AreaConfig
from repositories.areacache import AreaCache
from repositories.repositories import DATABASE
from services.eventservice import EventService


class AreaService:
    def __init__(self, event_service: EventService):
        self.repository = AreaCache(DATABASE)
        self.event_service = event_service

    def to_json_single(self, area, name):
        return {
            "id": area[0],
            "coverage_required": area[1],
            "x": area[2],
            "y": area[3],
            "width": area[4],
            "height": area[5],
            "camera_id": area[6],
            "name": name
        }

    def get_areas_json(self, camera_id=None):
        areas = self.repository.read_areas_for_one_camera(camera_id)
        areas = areas[0:4]

        names = self.get_area_names(areas)
        return [self.to_json_single(area, names[area]) for area in
                areas]

    def get_area_names(self, areas):
        result = {}
        if len(areas) > 0:
            result[areas[0]] = "A"
        if len(areas) > 1:
            result[areas[1]] = "B"
        if len(areas) > 2:
            result[areas[2]] = "C"
        if len(areas) > 3:
            result[areas[3]] = "D"
        return result

    def insert_events_for_areas(self, camera_id, camera_name, type, confidence, x, y, w, h):
        areas = self.repository.read_areas_for_one_camera(camera_id)
        if len(areas) == 0:
            self.event_service.insert_event(type, confidence, "A", camera_name)
        else:
            names = self.get_area_names(areas)
            for area in areas:
                area_config = AreaConfig.from_list(area)
                if area_config.fits(x, y, w, h):
                    self.event_service.insert_event(type, confidence, names[area], camera_name)

    def get_area_json(self, area_id):
        area = self.repository.read_area(area_id)
        camera_areas = self.repository.read_areas_for_one_camera(int(area[6]))
        names = self.get_area_names(camera_areas)
        for a in camera_areas:
            if int(a[0]) == int(area[0]):
                return self.to_json_single(area, names[a])

    def add_area(self, coverage_required, x, y, w, h, camera_id):
        return self.repository.insert_area(coverage_required, x, y, w, h, camera_id)

    def update_area(self, coverage_required, x, y, w, h, camera_id, name):
        self.repository.update_area(coverage_required, x, y, w, h, camera_id, name)

    def delete_area(self, id):
        self.repository.delete_area(id)

    @staticmethod
    def parse_areas(areas):
        jsons = []
        for area in areas:
            dic = {
                "name": area[0],
                "confidence_required": area[1],
                "x": area[2],
                "y": area[3],
                "width": area[4],
                "height": area[5],
                "camera_id": area[6]
            }
            jsons.append(dic)
        return jsons
