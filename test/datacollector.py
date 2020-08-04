import time
import cv2 as cv
from utils import ros


def collect():
    rosimg = ros.ROSImage()
    talker = rosimg.gen_talker('/ds/nav_cam/compressed')
    camera = cv.VideoCapture(1)
    while True:
        _, frame = camera.read()
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        talker.push(img)
        time.sleep(5)
