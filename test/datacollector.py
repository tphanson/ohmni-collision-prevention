import os
import datetime
import time
import cv2 as cv
from utils.ros import ROSImage

DESTINATION = '/storage/3115-7E1B/ds/'
FOLDER = datetime.datetime.now().strftime('%c')
os.mkdir(DESTINATION+FOLDER)


def calibrate():
    ros = ROSImage()
    talker = ros.gen_talker('/ds_calib/image/compressed')
    camera = cv.VideoCapture(1)
    count = 0
    while True:
        count += 1
        ok, img = camera.read()
        print("================== Image:", count, ok)
        if ok:
            talker.push(img)
        # Limit at 10Hz
        time.sleep(0.1)


def collect():
    camera = cv.VideoCapture(1)
    count = 0
    while True:
        count += 1
        ok, img = camera.read()
        if ok:
            name = DESTINATION+FOLDER+'/'+str(count)+'.jpg'
            print("================== Image:", name, ok)
            cv.imwrite(name, img)
        time.sleep(5)
