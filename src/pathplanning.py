import cv2 as cv
import numpy as np


class PathPlanning():
    def __init__(self, density=(14, 14)):
        self.density = density

    def draw_bitmap(self, mask):
        bitmap = cv.resize(mask, self.density)
        bitmap[6:8, 6:8] = np.zeros((2, 2))
        return np.ceil(bitmap)

    def neighbours(self, point):
        [y, x] = point
        return np.uniques([
            [max(0, y-1), max(0, x-1)],
            [max(0, y-1), x],
            [max(0, y-1), min(13, x+1)],
            [y, max(0, x-1)],
            [y, min(13, x+1)],
            [min(13, y+1), max(0, x-1)],
            [min(13, y+1), x],
            [min(13, y+1), min(13, x+1)],
        ])

    def a_star(self, bitmap):
        return None

    def dijkstra(self, bitmap):
        neighbours = self.neighbours((6, 6))
        print(neighbours)
        return None
