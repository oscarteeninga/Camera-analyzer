from config.areaconfig import AreaConfig
from repositories.repositories import DATABASE, AreasRepository
from services.eventservice import EventService


class AreaService:
    def __init__(self, event_service: EventService):
        self.repository = AreasRepository(DATABASE)
        self.event_service = event_service
        self.areas_cached = self.get_areas()

    def update(self):
        self.areas_cached = self.get_areas()

    def get_areas(self, camera_id=None):
        return [AreaConfig.from_list(l) for l in self.repository.read_areas(camera_id)]

    def get_areas_json(self, camera_id=None):
        return [area.to_json() for area in self.get_areas(camera_id)]

    def get_area(self, area_id):
        area = self.repository.read_area(area_id)
        return AreaConfig.from_list(area) if area else None

    def get_area_json(self, area_id):
        area = self.get_area(area_id)
        return area.to_json() if area else None

    def get_camera_image_coords_trimmed_to_areas(self, camera_id):
        areas_for_camera = list(filter(lambda a: a.camera_id == camera_id, self.areas_cached))
        if len(areas_for_camera) == 0:
            return None
        min_x = min(map(lambda a: a.x, areas_for_camera))
        min_y = min(map(lambda a: a.y, areas_for_camera))
        max_x = min(map(lambda a: a.x + a.width, areas_for_camera))
        max_y = min(map(lambda a: a.y + a.height, areas_for_camera))
        width = max_x - min_x
        height = max_y - min_y
        return min_x, min_y, width, height

    def change_absolute_coords_to_relative(self, camera_id):
        x, y, w, h = self.get_camera_image_coords_trimmed_to_areas(camera_id)
        areas_for_camera = list(filter(lambda a: a.camera_id == camera_id, self.areas_cached))
        return list(map(lambda area: area.copy_with_relative_coords(x, y), areas_for_camera))

    def insert_events_for_areas(self, camera_config, type, confidence, x, y, w, h):
        if camera_config.fit_video_to_areas:
            areas_for_camera = self.change_absolute_coords_to_relative(camera_config.id)
        else:
            areas_for_camera = list(
                filter(lambda a: a.camera_id == camera_config.id, self.areas_cached))
        for area in areas_for_camera:
            if area.fits(x, y, w, h):
                self.event_service.insert_event(type, confidence, area.name, camera_config.name)

    def insert_area(self, coverage_required, x, y, w, h, camera_id):
        self.repository.insert_area(coverage_required, x, y, w, h, camera_id)
        self.update()

    def update_area(self, id, coverage_required, x, y, w, h):
        self.repository.update_area(id, coverage_required, x, y, w, h)
        self.update()

    def delete_area(self, id):
        self.repository.delete_area(id)
        self.update()
