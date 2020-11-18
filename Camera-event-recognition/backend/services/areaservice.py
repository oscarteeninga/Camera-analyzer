from config.areaconfig import AreaConfig
from repositories.repositories import AreasRepository, DATABASE
from services.cacheservice import cache, Dictionaries
from services.cameraservice import CameraService

camera_service = CameraService()


class AreaService:
    def __init__(self):
        self.repository = AreasRepository(DATABASE)

    def get_areas(self, camera_id=None):
        return [AreaConfig.from_list(l) for l in self.repository.read_areas(camera_id)]

    def get_areas_json(self, camera_id=None):
        return [area.to_json() for area in self.get_areas(camera_id)]

    def get_area(self, camera_id, area_name):
        areas = self.get_areas(camera_id)
        for area in areas:
            if area.name == area_name:
                return area
        return None

    def get_area_json(self, camera_id, area_name):
        area = self.get_area(camera_id, area_name)
        return area.to_json() if area else None

    def recognize_area(self, x, y, width, height):
        areas = cache.get(Dictionaries.AREAS)
        #DOWYJEBANIA
        for area in areas:
            detect_box = AreaConfig(area.get('name'), float(area.get('x')), float(area.get('y')),
                                    float(area.get('width')), float(area.get('height')))
            if float(area.get('confidence_required')) <= detect_box.coverage(x, y, width, height):
                return area.get('name')

    def add_area(self, name, confidence_required, x, y, w, h, camera_id):
        self.repository.insert_area(name, confidence_required, x, y, w, h, camera_id)
        cache.set(Dictionaries.AREAS, self.get_areas())

    def update_area(self, new_name, confidence_required, x, y, w, h, camera_id, name):
        self.repository.update_area(new_name, confidence_required, x, y, w, h, camera_id, name)
        cache.set(Dictionaries.AREAS, self.get_areas())

    def delete_area(self, id, name):
        self.repository.delete_area(id, name)

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
