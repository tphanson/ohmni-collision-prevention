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
            print("================== Image No:", count)
            cv.imwrite(DESTINATION+str(count)+'.jpg', img)
        time.sleep(5)
