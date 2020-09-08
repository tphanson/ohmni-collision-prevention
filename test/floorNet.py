import time
import cv2 as cv
import numpy as np

from utils import ros, odometry
from src.floorNet import FloorNet

BOX = (50, 10)
CENTROID = (112, 80)
(XMIN, XMAX, YMIN, YMAX) = (
    int(CENTROID[0] - BOX[0]/2), int(CENTROID[0]+BOX[0]/2),
    int(CENTROID[1] - BOX[1]), int(CENTROID[1])
)
COLOR_RED = [0, 0, 255]
OPACITY = 0.5


def infer(botshell, debug=False):
    # Init modules
    floorNet = FloorNet()
    odo = odometry.Odometry(floorNet.image_shape)
    if debug:
        rosimg = ros.ROSImage()
        talker = rosimg.gen_talker('/ocp/draw_image/compressed')
    camera = cv.VideoCapture(1)
    # Prediction
    while True:
        start = time.time()
        print("======================================")

        # Infer
        _, frame = camera.read()
        print('*** Debug camera shape:', frame.shape)
        img, mask = floorNet.predict(frame)
        img = (img*127.5+127.5)/255
        # Detect collision
        detector = mask[YMIN:YMAX, XMIN:XMAX]
        area = (YMAX-YMIN)*(XMAX-XMIN)
        collision = np.sum(detector)
        confidence = collision/area
        if confidence > 0.2:
            print('Stop it, idiots!', confidence)
            botshell.sendall(b'manual_move -500 500\n')
        else:
            botshell.sendall(b'manual_move 0 0\n')
        # Visualize
        if debug:
            # mask[YMIN:YMAX, XMIN:XMAX] = mask[YMIN:YMAX, XMIN:XMAX] + 0.5
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            img = cv.addWeighted(mask, OPACITY, img, 1-OPACITY, 0)
            polygon = odo.generate_driving_zone(1000, np.pi)
            img = img * 255
            img = cv.fillPoly(img, [polygon], COLOR_RED)
            talker.push(img)

        # Calculate frames per second (FPS)
        end = time.time()
        fps = 1/(end-start)
        print('Total estimated time: {:.4f}'.format(end-start))
        print("FPS: {:.1f}".format(fps))

    talker.stop()
    rosimg.stop()
