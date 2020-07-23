import time
import cv2 as cv

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
        ret, frame = camera.read()
        print("Debug", ret)
        img, mask = floorNet.predict(frame)
        # Visualize
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        cv.addWeighted(mask, 0.5, img, 0.5, 0, img)
        rosimg.apush(frame)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))
