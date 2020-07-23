import time
import cv2 as cv
import numpy as np

from utils import ros
from src.floorNet import FloorNet

BOX = (40, 40)
CENTROID = (112, 112)
(XMIN, XMAX, YMIN, YMAX) = (
    int(CENTROID[0] - BOX[0]/2), int(CENTROID[0]+BOX[0]/2),
    int(CENTROID[1] - BOX[1]), int(CENTROID[1])
)


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
        img, mask = floorNet.predict(frame)
        # Detect collision
        detector = mask[YMIN:YMAX, XMIN:XMAX]
        area = (YMAX-YMIN)*(XMAX-XMIN)
        collision = np.sum(detector)
        print(collision, area, collision/area)
        # Visualize
        if debug:
            mask[YMIN:YMAX, XMIN:XMAX] = mask[YMIN:YMAX, XMIN:XMAX] + 0.5
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            cv.addWeighted(mask, 0.5, img, 0.5, 0, mask)
            rosimg.apush(mask * 255)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))
