import numpy as np
import math
import cv2 as cv

BOT_WIDTH = 450
BOT_CENTER = [100, -100]

CAMERA_MATRIX = np.array([[0.4315, 0, 0.4695], [0, 0.7674, 0.5099], [0, 0, 1]])
RVEC = np.array([-np.deg2rad(11), 0, 0])
TVEC = np.array([0, 0, 1192.01])
DISTORTION_COEFF = np.array(
    [0.7365, 0.2228, 0, 0.0002, 0.0074, 1.097, 0.4153, 0.0477])


class Odometry:
    def __init__(self, image_shape, num_of_samples=100):
        self.image_shape = image_shape
        self.num_of_samples = num_of_samples

    def _distort(self, pts, image_size):
        (h, w) = image_size
        pts, _ = cv.projectPoints(
            pts, RVEC, TVEC, CAMERA_MATRIX, DISTORTION_COEFF)
        pts[..., 0] = pts[..., 0]*w
        pts[..., 1] = pts[..., 1]*h
        return pts.squeeze().astype(np.int32)

    def _generate_ring(self, R, center, rad=math.pi):
        stop = int(R*math.cos(math.pi-rad))
        x = np.linspace(-R, stop, self.num_of_samples)
        y = -np.sqrt(np.square(np.full(self.num_of_samples, R)) - np.square(x))
        x = x + center[0]
        y = y + center[1]
        z = np.zeros(self.num_of_samples)
        return np.stack((x, y, z), axis=-1)

    def generate_driving_zone(self, R, rad):
        center = np.array([R, 0]) + BOT_CENTER
        outer_pts = self._generate_ring(
            R + np.sign(R)*BOT_WIDTH/2, center, rad)
        outer_pts = self._distort(outer_pts, self.image_shape)
        inner_pts = self._generate_ring(
            R - np.sign(R)*BOT_WIDTH/2, center, rad)
        inner_pts = self._distort(inner_pts, self.image_shape)
        polygon = np.append(inner_pts, np.flip(outer_pts, axis=0), axis=0)
        return polygon
