import time
import cv2 as cv

# It may be changed with other devices
USB_PATH = '/mnt/media_rw/3115-7E1B/ds/'


def collect():
    camera = cv.VideoCapture(2)
    count = 0
    while True:
        count += 1
        ok, img = camera.read()
        if ok:
            cv.imwrite(USB_PATH+str(count)+'.jpg', img)
        time.sleep(5)
