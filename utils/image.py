import numpy as np
import cv2 as cv

CAMERA_MATRIX = np.array([[552.4031/1280, 0, 600.9664/1280],
                          [0, 552.51119/720, 367.1639/720],
                          [0, 0, 1]])
DISTORTION_COEFFICIENCES = np.array(
    [0.736478, 0.222831, 0, 0, 0, 1.097010, 0.415286, 0.047720])


def undistort(img):
    """ Only for Ohmni's nav camera """
    camera_matrix = np.copy(CAMERA_MATRIX)
    camera_matrix[0] = camera_matrix[0] * img.shape[1]
    camera_matrix[1] = camera_matrix[1] * img.shape[0]
    print(camera_matrix, img.shape)
    undistort_img = cv.undistort(img, camera_matrix, DISTORTION_COEFFICIENCES)
    return undistort_img
