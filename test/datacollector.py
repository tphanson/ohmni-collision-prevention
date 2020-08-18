import time
import cv2 as cv

DESTINATION = '../ds/'


def collect():
    camera = cv.VideoCapture(2)
    count = 0
    while True:
        count += 1
        print("================== Image No:", count)
        ok, img = camera.read()
        if ok:
            cv.imwrite(DESTINATION+str(count)+'.jpg', img)
        time.sleep(5)
