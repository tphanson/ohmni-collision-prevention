import time
import cv2 as cv
from utils import ros


def collect():
    rosimg = ros.ROSImage()
    rosimg.client.run()
    camera = cv.VideoCapture(1)

    while True:
        _, frame = camera.read()
        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        rosimg.apush(img)
        time.sleep(5)
