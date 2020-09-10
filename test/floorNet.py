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
        # Get images
        _, frame = camera.read()
        print('*** Debug camera shape:', frame.shape)
        # Get velocities
        botshell.sendall(b'get_velocity\n')
        vleft, vright = 0, 0
        try:
            data = botshell.recv(1024)
            [lvel, angvel] = data.decode('utf8').split(',')
            lvel, angvel = float(lvel), float(angvel)
            vleft = np.abs(int(800 * lvel + 450 * angvel))
            vright = np.abs(int(800 * -lvel + 450 * angvel))
        except ValueError:
            pass
        print('*** Debug velocities:', vleft, vright)
        # Infer
        img, mask = floorNet.predict(frame)
        img = (img*127.5+127.5)/255
        # Detect collision
        # Add a fraction to R to prevent zero division
        R = 225 * (vleft + vright) / (vright - vleft + 0.000001)
        print('*** Debug R:', R)
        driving_zone = odo.generate_driving_zone(R, np.pi)
        bool_mask = image.get_mask_by_polygon(img, driving_zone)
        confidence = np.sum(mask[bool_mask])/np.sum(bool_mask)
        print('*** Debug confidence:', confidence)
        if confidence > 0.2:
            print('Stop it, idiots!', confidence)
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
