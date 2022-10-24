import cv2 as cv
import matplotlib.pyplot as plt

image = cv.imread('origin.jpg', cv.IMREAD_GRAYSCALE)
image_eq = cv.equalizeHist(image)
cv.imwrite('histogram_equalization.jpg', image_eq)
hist_origin = cv.calcHist([image], [0], None, [256], [0, 256])
hist_eq = cv.calcHist([image_eq], [0], None, [256], [0, 256])
hists = [hist_origin.reshape(256), hist_eq.reshape(256)]
title = ["histogram origin", "histogram equalization"]
fig = plt.figure(figsize = (9, 4) ) 
for i in range(2): 
    h = hists[i]
    fig.add_subplot(1, 2, i + 1)
    plt.bar(range(0, 256), h)
    plt.title("{}".format(title[i]))
plt.savefig('histogram_compare.jpg')
