import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

image_path = './debug.jpg'
img = cv.imread(image_path)
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

(w, h, _) = img.shape
x = np.arange(0, w)
y = np.arange(0, h)

cx = w/2
cy = h/2
r = 25.

# The two lines below could be merged, but I stored the mask
# for code clarity.
anchor = (x[np.newaxis, :]-cx)**2 + (y[:, np.newaxis]-cy)**2
mask = np.bitwise_and(anchor <= r**2, anchor > (r-1)**2)
img[mask] = [255, 0, 0]

plt.imshow(img)
plt.show()
