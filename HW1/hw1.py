import cv2

img = cv2.imread("origin.jpg")
img1 = cv2.resize(img, None ,fx = 0.2, fy = 0.2, interpolation = cv2.INTER_LINEAR)
img2 = cv2.resize(img, None ,fx = 5, fy = 5, interpolation = cv2.INTER_LINEAR)
img3 = cv2.resize(img, None ,fx = 32, fy = 32, interpolation = cv2.INTER_LINEAR)
img4 = cv2.resize(img, None ,fx = 0.2, fy = 0.2, interpolation = cv2.INTER_CUBIC)
img5 = cv2.resize(img, None ,fx = 5, fy = 5, interpolation = cv2.INTER_CUBIC)
img6 = cv2.resize(img, None ,fx = 32, fy = 32, interpolation = cv2.INTER_CUBIC)


cv2.imwrite("bilinear_0.2.jpg", img1)
cv2.imwrite("bilinear_5.jpg", img2)
cv2.imwrite("bilinear_32.jpg", img3)
cv2.imwrite("bicubic_0.2.jpg", img4)
cv2.imwrite("bicubic_5.jpg", img5)
cv2.imwrite("bicubic_32.jpg", img6)
