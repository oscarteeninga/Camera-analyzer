from model.receiver import DetectBox
from repositories.repositories import AreasRepository, DATABASE
from services.cameraservice import CameraService

camera_service = CameraService()


class AreaService:
    def __init__(self):
        self.repository = AreasRepository(DATABASE)

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
        return None

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
                "camera": camera_service.get_camera_name(area[6], api=True)
            }
            jsons.append(dic)
        return jsons
