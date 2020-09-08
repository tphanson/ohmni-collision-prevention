import numpy as np
import cv2 as cv

COLOR_RED = [0, 0, 255]
OPACITY = 0.5


def draw_polygon(img, polygon):
    mask = np.zeros(img.shape, dtype=img.dtype)
    mask = cv.fillPoly(mask, [polygon], COLOR_RED)
    red_mask = np.full(img.shape, COLOR_RED, dtype=img.dtype)
    bool_mask = np.equal(mask, red_mask).all(axis=2)
    img[bool_mask] = img[bool_mask] * \
        (1-OPACITY) + np.array(COLOR_RED) * OPACITY
    return img
