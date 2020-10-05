import cv2 as cv
import numpy as np


def draw_bitmap(mask, density=(14, 14)):
    bitmap = cv.resize(mask, density)
    bitmap[6:8, 6:8] = np.zeros((2, 2))
    return np.ceil(bitmap)


def a_star(bitmap):
    return None
