import time
import cv2 as cv
from utils import ros


def client_collect():
    rosimg = ros.ROSImage()
    talker = rosimg.gen_talker('/ds/nav_cam/compressed')
    camera = cv.VideoCapture(1)
    while True:
        _, frame = camera.read()
        talker.push(frame)
        time.sleep(5)


def host_collect():
    rosimg = ros.ROSImage(host='192.168.123.53')
    listener = rosimg.gen_listener('/ds/nav_cam/compressed')
    _, img = listener.get()
    cv.imshow('Video', img)
    if cv.waitKey(10) & 0xFF == ord('q'):
            break
