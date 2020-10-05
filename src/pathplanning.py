import cv2 as cv
import numpy as np


def draw_bitmap(mask, density=(14, 14)):
    bitmap = cv.resize(mask, density)
    return np.ceil(bitmap)

def a_star(bitmap):
    return None