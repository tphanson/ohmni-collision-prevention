import time
import cv2 as cv
import numpy as np

from utils import ros, odometry, image, simulation
from src.floorNet import FloorNet


def infer(botshell, debug=False):
    # Init modules
    floorNet = FloorNet()
    odo = odometry.Odometry(floorNet.image_shape)
    if debug:
        rosimg = ros.ROSImage()
        talker = rosimg.gen_talker('/ocp/draw_image/compressed')
    camera = cv.VideoCapture(1)
    simulation.simMovement()

    # Prediction
    while True:
        start = time.time()
        print("======================================")
        # Get images
        _, frame = camera.read()
        print('*** Debug camera shape:', frame.shape)
        # Get velocities
        socstart = time.time()
        botshell.sendall(b'get_velocity\n')
        vleft, vright = 0, 0
        try:
            data = botshell.recv(1024)
            [lvel, angvel] = data.decode('utf8').split(',')
            lvel, angvel = float(lvel), float(angvel)
            vleft = np.abs(800 * lvel + 450 * angvel)
            vright = np.abs(800 * lvel - 450 * angvel)
            if angvel <= 0:
                vleft, vright = 0, 0
        except ValueError:
            pass
        socend = time.time()
        print('Socket estimated time: {:.4f}'.format(socend-socstart))
        # Infer
        img, mask = floorNet.predict(frame)
        img = (img*127.5+127.5)/255
        # Detect collision
        # Add a fraction to the denominator to prevent zero division
        cpstart = time.time()
        R = np.round(225 * (vright + vleft) / (vleft - vright + 0.0001))
        Rad = np.pi if np.abs(R) < 400 else 400*np.pi/np.abs(R)
        print('*** Debug R, Radian:', R, Rad)
        driving_zone = odo.generate_driving_zone(R, Rad)
        bool_mask = image.get_mask_by_polygon(img, driving_zone)
        # Munis 1 for the case of R=0
        confidence = (np.sum(mask[bool_mask])-1)/np.sum(bool_mask)
        print('*** Debug confidence:', confidence)
        cpend = time.time()
        print('Collision pred estimated time: {:.4f}'.format(cpend-cpstart))
        if confidence > 0.05:
            print('Stop it, idiots!', confidence)
            botshell.sendall(b'manual_move 1 -1\n')
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
