import time
import cv2 as cv

DESTINATION = '../ds/'


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
