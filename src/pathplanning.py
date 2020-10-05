import cv2 as cv
import numpy as np


def create_map(mask, density=(14, 14)):
    _map = cv.resize(mask, density)
    print(_map)
    return _map
