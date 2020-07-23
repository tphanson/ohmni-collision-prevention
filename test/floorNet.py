import time
import cv2 as cv
import numpy as np

from utils import ros
from src.floorNet import FloorNet


def infer():
    # Init modules
    floorNet = FloorNet()
    rosimg = ros.ROSImage()
    rosimg.client.run()
    camera = cv.VideoCapture(1)
    # Prediction
    while True:
        start = time.time()
        print("======================================")
        # Infer
        _, frame = camera.read()
        img, mask = floorNet.predict(frame)
        # Visualize
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        collision = np.zeros(mask.shape, dtype=np.float32)
        cv.line(collision, (90, 90), (134, 90), (0, 0, 255), 15)
        collision = collision/255
        # cv.addWeighted(mask, 0.5, collision, 0.5, 0, collision)

        rosimg.apush(collision)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))
