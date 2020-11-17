from config.areaconfig import AreaConfig
from repositories.repositories import AreasRepository, DATABASE
from services.cacheservice import cache, Dictionaries
from services.cameraservice import CameraService

camera_service = CameraService()


class AreaService:
    def __init__(self):
        self.repository = AreasRepository(DATABASE)

    def get_areas(self, id=None, name=None):
        database_areas = self.repository.read_areas(id, name)
        return self.parse_areas(database_areas)

    def recognize_area(self, x, y, width, height):
        areas = cache.get(Dictionaries.AREAS)
        for area in areas:
            detect_box = AreaConfig(area.get('name'), float(area.get('x')), float(area.get('y')),
                                    float(area.get('width')), float(area.get('height')))
            if float(area.get('confidence_required')) <= detect_box.coverage(x, y, width, height):
                return area.get('name')
        return None

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
