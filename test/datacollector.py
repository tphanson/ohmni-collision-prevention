import time
import cv2 as cv
from utils.ros import ROSImage

DESTINATION = '../ds/'


def calibrate():
    ros = ROSImage()
    talker = ros.gen_talker('/ds_calib/image/compressed')
    camera = cv.VideoCapture(2)
    count = 0
    while True:
        count += 1
        print("================== Image:", count)
        ok, img = camera.read()
        if ok:
            talker.push(img)
        # Limit 20Hz
        time.sleep(0.1)

def collect():
    camera = cv.VideoCapture(2)
    count = 0
    while True:
        count += 1
        ok, img = camera.read()
        if ok:
            name = DESTINATION+str(count)+'.jpg'
            print("================== Image:", name)
            cv.imwrite(name, img)
        time.sleep(5)
