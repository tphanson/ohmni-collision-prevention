import time
import cv2 as cv
import numpy as np

from utils import ros, odometry, image
from src.floorNet import FloorNet
from src.pathplanning import PathPlanning

DIVISION = 14  # 7*2^x
SOURCE = [DIVISION/2, DIVISION/2]
DESTINATION = [DIVISION/2, 0]


def infer(botshell, debug=False):
    # Init modules
    floorNet = FloorNet()
    pp = PathPlanning(DIVISION)
    odo = odometry.Odometry(botshell, floorNet.image_shape)
    if debug:
        rosimg = ros.ROSImage()
        talker = rosimg.gen_talker('/ocp/draw_image/compressed')
    camera = cv.VideoCapture(1)

    # Prediction
    while True:
        start = time.time()
        print("======================================")
        # Get images
        _, frame = camera.read()
        print('*** Debug camera shape:', frame.shape)
        # Infer
        img, mask = floorNet.predict(frame)
        img = (img*127.5+127.5)/255
        # Path planning
        bitmap = pp.draw_bitmap(mask)
        ppstart = time.time()
        trajectory = pp.dijkstra(bitmap, SOURCE, DESTINATION)
        ppend = time.time()
        print('Path planning estimated time: {:.4f}'.format(ppend-ppstart))
        # Visualize
        if debug:
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            img = cv.addWeighted(mask, 0.5, img, 0.5, 0)
            img = img * 255
            if trajectory is not None:
                points = np.array(trajectory, dtype=np.int32)*224/DIVISION
                img = image.draw_trajectory(img, points)
            talker.push(img)

        # Calculate frames per second (FPS)
        end = time.time()
        fps = 1/(end-start)
        print('Total estimated time: {:.4f}'.format(end-start))
        print("FPS: {:.1f}".format(fps))

    talker.stop()
    rosimg.stop()
