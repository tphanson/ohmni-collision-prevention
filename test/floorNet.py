import time
import cv2 as cv

from utils.camera import Camera
from src.floorNet import FloorNet


def infer():
    # Image source
    cam = Camera()
    stream = cam.get_stream()
    floorNet = FloorNet()
    # Prediction
    while True:
        start = time.time()
        print("======================================")
        # Infer
        raw_img = stream.get()
        img, mask = floorNet.predict(raw_img)
        # Visualize
        mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        cv.addWeighted(mask, 0.5, img, 0.5, 0, img)
        cv.imshow('Camera', img)

        # Calculate frames per second (FPS)
        end = time.time()
        print('Total estimated time: {:.4f}'.format(end-start))
        fps = 1/(end-start)
        print("FPS: {:.1f}".format(fps))

        if cv.waitKey(10) & 0xFF == ord('q'):
            break
    # Clear resources
    cv.destroyAllWindows()
    cam.terminate()
