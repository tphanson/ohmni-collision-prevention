import cv2 as cv
from utils import ros


rosimg = ros.ROSImage(host='192.168.123.53')
listener = rosimg.gen_listener('/ds/nav_cam/compressed')
while True:
    _, img = listener.get()
    cv.imshow('Video', img)
    if cv.waitKey(5000) & 0xFF == ord('q'):
        break
