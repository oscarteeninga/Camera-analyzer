import numpy as np


class AreaConfig:
    def __init__(self, id, name, coverage_required, x, y, width, height, camera_id):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.coverage_required = float(coverage_required)
        self.camera_id = camera_id

        self.color = np.random.uniform(0, 255, 3)

    @staticmethod
    def from_list(l):
        return AreaConfig(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7])

    @staticmethod
    def field(a, b):
        if min(a, b) < 0:
            return 0
        else:
            return a * b

    def fits(self, x, y, w, h):
        return self.coverage(x, y, w, h) >= self.coverage_required

    def coverage(self, x, y, width, height):
        if self.width + self.height == 0:
            return 1.0
        else:
            x1 = max(self.x, x)
            y1 = max(self.y, y)
            x2 = min(self.x + self.width, x + width)
            y2 = min(self.y + self.height, y + height)
            common_width = (x2 - x1)
            common_height = (y2 - y1)
            return self.field(common_width, common_height) / self.field(width, height)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "confidence_required": self.coverage_required,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "camera_id": self.camera_id
        }