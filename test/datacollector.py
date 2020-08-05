import time
import cv2 as cv
from utils import ros


def collect():
    rosimg = ros.ROSImage()
    talker = rosimg.gen_talker('/ds/nav_cam/compressed')
    camera = cv.VideoCapture(2)
    while True:
        _, frame = camera.read()
        talker.push(frame)
        time.sleep(5)
