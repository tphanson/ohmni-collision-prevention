import time
import cv2 as cv
import numpy as np

from utils import ros
from src.floorNet import FloorNet


def infer(debug=False):
    # Init modules
    floorNet = FloorNet()
    if debug:
        rosimg = ros.ROSImage()
        rosimg.client.run()
    camera = cv.VideoCapture(1)
    # Prediction
    while True:
        start = time.time()
        print("======================================")
        # Infer
        _, frame = camera.read()
        _, mask = floorNet.predict(frame)
        # Detect collision
        detector = mask[90:110, 85:139]
        area = (139-85)*(110-90)
        collision = np.sum(detector)
        print(collision, area, collision/area)
        # Visualize
        if debug:
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR) * 255
            collision = np.zeros(mask.shape, dtype=np.float32)
            cv.line(collision, (85, 100), (139, 100), (0, 0, 255), 20)
            cv.addWeighted(mask, 0.5, collision, 0.5, 0, mask)
            img = img * 255
            cv.addWeighted(mask, 0.5, img, 0.5, 0, mask)
            rosimg.apush(mask)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))
