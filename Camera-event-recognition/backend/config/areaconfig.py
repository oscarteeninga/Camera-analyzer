import numpy as np


class AreaConfig:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.width = width
        self.y = y
        self.height = height

        self.color = np.random.uniform(0, 255, 3)

    @staticmethod
    def from_list(l):
        return AreaConfig(l[1], l[2], l[3], l[4], l[5])

    @staticmethod
    def field(a, b):
        if min(a, b) < 0:
            return 0
        else:
            return a * b

    def coverage(self, x, y, width, height):
        x1 = max(self.x, x)
        y1 = max(self.y, y)
        x2 = min(self.x + self.width, x + width)
        y2 = min(self.y + self.height, y + height)
        common_width = (x2 - x1)
        common_height = (y2 - y1)
        return self.field(common_width, common_height) / self.field(width, height)