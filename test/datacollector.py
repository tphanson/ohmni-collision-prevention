import os
import datetime
import time
import cv2 as cv
from utils.ros import ROSImage

USB_PATH = '/storage/3115-7E1B/ds/'
DESTINATION = datetime.datetime.now().strftime(
    '%c').replace(' ', '_').replace(':', '_')
os.mkdir(USB_PATH+DESTINATION)


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
        time.sleep(5)


def collect():
    camera = cv.VideoCapture(1)
    count = 0
    while True:
        count += 1
        ok, img = camera.read()
        name = USB_PATH + DESTINATION + '/' + str(count) + '.jpg'
        print("================== Image:", name, ok)
        if ok:
            cv.imwrite(name, img)
        time.sleep(5)
