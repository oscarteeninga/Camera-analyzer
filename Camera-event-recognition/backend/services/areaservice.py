from config.areaconfig import AreaConfig
from repositories.repositories import AreasRepository, DATABASE
from services.cacheservice import cache, Dictionaries
from services.cameraservice import CameraService

camera_service = CameraService()


class AreaService:
    def __init__(self):
        self.repository = AreasRepository(DATABASE)

    def get_areas(self):
        database_areas = self.repository.read_areas()
        return self.parse_areas(database_areas)

    def recognize_area(self, x, y, width, height):
        areas = cache.get(Dictionaries.AREAS)
        for area in areas:
            detect_box = AreaConfig(area.get('name'), float(area.get('x')), float(area.get('y')), float(area.get('width')), float(area.get('height')))
            if float(area.get('confidence_required')) <= detect_box.coverage(x, y, width, height):
                return area.get('name')
        return None

    def add_area(self, name, confidence_required, x, y, w, h, camera_name):
        camera_id = cache.get(Dictionaries.CAMERA_NAME_TO_IP).get(camera_name)
        self.repository.insert_area(name, confidence_required, x, y, w, h, camera_id)
        cache.set(Dictionaries.AREAS, self.get_areas())

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
                "camera": cache.get(Dictionaries.CAMERA_IP_TO_NAME).get(area[6])
            }
            jsons.append(dic)
        return jsons
