from config.areaconfig import AreaConfig
from repositories.repositories import AreasRepository, DATABASE
from services.cameraservice import CameraService

camera_service = CameraService()


class AreaService:
    def __init__(self):
        self.repository = AreasRepository(DATABASE)

    def get_areas(self):
        database_areas = self.repository.read_areas()
        return self.parse_areas(database_areas)

    def get_area(self, camera):
        return self.repository.read_area(camera)

    def recognize_area(self, x, y, width, height):
        areas = self.repository.read_areas()
        for area in areas:
            detect_box = AreaConfig.from_list(area)
            if float(area[1]) <= detect_box.coverage(x, y, width, height):
                return area[0]
        return None

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
                "camera": camera_service.get_camera_name(area[6])
            }
            jsons.append(dic)
        return jsons
