import time
import cv2 as cv
import numpy as np

from utils import ros
from src.floorNet import FloorNet

BOX = (50, 2)
CENTROID = (112, 90)
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
    # camera.set(3, 224)
    # camera.set(4, 224)
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
        confidence = collision/area
        if confidence > 0.2:
            print('Stop it, idiots!', confidence)
            botshell.sendall(b'manual_move 1 1\n')
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
