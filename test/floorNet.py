import time
import cv2 as cv
import numpy as np

from utils import ros, odometry, image
from src.floorNet import FloorNet


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
        driving_zone = odo.generate_driving_zone(1000, np.pi)
        bool_mask = image.get_mask_by_polygon(img, driving_zone)
        confidence = np.sum(mask[bool_mask])/np.sum(bool_mask)
        print('*** Debug confidence:', confidence)
        if confidence > 0.2:
            print('Stop it, idiots!', confidence)
            botshell.sendall(b'get_velocity\n')
            data = botshell.recv(1024)
            print('Received', data, type(data))
            # botshell.sendall(b'manual_move -500 500\n')
        else:
            botshell.sendall(b'manual_move 0 0\n')
        # Visualize
        if debug:
            mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            img = cv.addWeighted(mask, 0.5, img, 0.5, 0)
            img = img * 255
            img = image.draw_polygon(img, driving_zone)
            talker.push(img)

        # Calculate frames per second (FPS)
        end = time.time()
        fps = 1/(end-start)
        print('Total estimated time: {:.4f}'.format(end-start))
        print("FPS: {:.1f}".format(fps))

    talker.stop()
    rosimg.stop()
