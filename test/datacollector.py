import time
import cv2 as cv
from utils import ros


def collect():
    rosimg = ros.ROSImage()
    talker = rosimg.gen_talker('/ds/nav_cam/compressed')
    camera = cv.VideoCapture(1)
    while True:
        _, frame = camera.read()
        talker.push(frame)
        time.sleep(5)y(5000) & 0xFF == ord('q'):
            break
