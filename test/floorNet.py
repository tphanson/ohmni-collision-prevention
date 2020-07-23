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
        _, mask = floorNet.predict(frame)
        # Visualize
        # mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR) * 255
        mask = mask * 255
        collision = np.zeros(mask.shape, dtype=np.float32)
        cv.line(collision, (90, 100), (134, 100), (0, 0, 255), 20)
        cv.addWeighted(mask, 0.5, collision, 0.5, 0, mask)

        rosimg.apush(mask)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))
