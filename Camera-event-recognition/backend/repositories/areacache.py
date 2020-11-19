from repositories.repositories import AreasRepository


class AreaCache(AreasRepository):

    def __init__(self, data_base):
        super().__init__(data_base)
        self.areas = super().read_areas()

    def insert_area(self, confidence_required, x, y, w, h, camera_id):
        super().insert_area(confidence_required, x, y, w, h, camera_id)
        self.areas = super().read_areas()

    def update_area(self, id, confidence_required, x, y, w, h, camera_id):
        super().update_area(id, confidence_required, x, y, w, h, camera_id)
        self.areas = super().read_areas()

    def delete_area(self, id):
        super().delete_area(id)
        self.areas = super().read_areas()

    def read_areas(self):
        return self.areas

    def read_areas_for_one_camera(self, camera_id):
        a = []
        for area in self.areas:
            if int(area[6]) == int(camera_id):
                a.append(area)
        return a

    def read_areas_db(self):
        return super().read_areas()

    def read_area(self, id):
        for area in self.areas:
            if int(area[0]) == int(id):
                return area
