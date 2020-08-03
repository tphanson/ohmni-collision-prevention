import time
import cv2 as cv
import numpy as np

from utils import ros
from src.floorNet import FloorNet

BOX = (50, 1)
AREA = BOX[0]*BOX[1]
WARNING_CENTROID = (112, 80)
DANGER_CENTROID = (112, 90)
(WARNING_XMIN, WARNING_XMAX, WARNING_YMIN, WARNING_YMAX) = (
    int(WARNING_CENTROID[0] - BOX[0]/2), int(WARNING_CENTROID[0]+BOX[0]/2),
    int(WARNING_CENTROID[1] - BOX[1]), int(WARNING_CENTROID[1])
)
(DANGER_XMIN, DANGER_XMAX, DANGER_YMIN, DANGER_YMAX) = (
    int(DANGER_CENTROID[0] - BOX[0]/2), int(DANGER_CENTROID[0]+BOX[0]/2),
    int(DANGER_CENTROID[1] - BOX[1]), int(DANGER_CENTROID[1])
)


def infer(botshell, debug=False):
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
        # Dangerous level
        danger_detector = mask[DANGER_YMIN:DANGER_YMAX,
                               DANGER_XMIN:DANGER_XMAX]
        danger_collision = np.sum(danger_detector)
        danger_confidence = danger_collision/AREA
        # Warning level
        warning_detector = mask[WARNING_YMIN:WARNING_YMAX,
                                WARNING_XMIN:WARNING_XMAX]
        warning_collision = np.sum(warning_detector)
        warning_confidence = warning_collision/AREA
        if danger_confidence > 0.2:
            print('Dangerous level:', danger_confidence)
            botshell.sendall(b'manual_move -500 500\n')
        elif warning_confidence > 0.2:
            print('Warning level:', warning_confidence)
            botshell.sendall(b'manual_move 1 1\n')
        else:
            botshell.sendall(b'manual_move 0 0\n')
        # Visualize
        if debug:
            # mask[YMIN:YMAX, XMIN:XMAX] = mask[YMIN:YMAX, XMIN:XMAX] + 0.5
            # mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            # cv.addWeighted(mask, 0.5, img, 0.5, 0, mask)
            rosimg.apush(mask * 255)

        # Calculate frames per second (FPS)
        end = time.time()
        fps = 1/(end-start)
        print('Total estimated time: {:.4f}'.format(end-start))
        print("FPS: {:.1f}".format(fps))
