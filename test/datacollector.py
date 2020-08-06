import time
import cv2 as cv


def collect():
    camera = cv.VideoCapture(2)
    while True:
        ok, frame = camera.read()
        if ok:
            print(frame.shape)
        time.sleep(5)
