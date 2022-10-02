import cv2 as cv
import numpy as np
import math

def w(x, a = -0.5):
    if abs(x) <= 1:
        return (a + 2) * (abs(x) ** 3) - (a + 3) * (abs(x) ** 2) + 1 
    elif abs(x) > 1 and abs(x) < 2:
        return a * (abs(x) ** 3) - (5 * a) * (abs(x) ** 2) + 8 * a * abs(x) - 4 * a
    else:
        return 0
def pad_arrond(image):
    row, col, dim = image.shape
    pad_image = np.zeros((row + 4, col + 4, dim))
    pad_image[2:row + 2, 2:col + 2] = image #middle
    pad_image[2:row + 2, 0:2]=image[:, 0:1] #left
    pad_image[2:row + 2, col + 2:col + 4]=image[:, col - 1:col] #right
    pad_image[0:2, 2:col + 2]=image[0:1, :] #top
    pad_image[row + 2:row + 4, 2:col + 2]=image[row - 1: row, :] #down
    pad_image[0:2, 0:2]=img[0, 0] #top-left
    pad_image[0:2, col + 2:col + 4]=img[0,col - 1] #top-right
    pad_image[row + 2:row + 4, 0:2]=img[row - 1,0] #down-left
    pad_image[row + 2:row + 4, col + 2:col + 4]=img[row - 1,col - 1]#down-right
    return pad_image

def bicubic(image, scaling_factor):
    row, col, dim = image.shape
    #pad around incase next step out of boundry
    image = pad_arrond(image)
    new_row = int(row * scaling_factor)
    new_col = int(col * scaling_factor)
    # create new image
    result = np.zeros((new_row, new_col, dim))
    # mapping to origin image
    
    for k in range(dim):
        for i in range(new_row):
            for j in range(new_col):
                x = i / scaling_factor
                y = j / scaling_factor
                
                #計算要 bicubic Interpolation 的四條線
                x_floor = math.floor(x)
                x_ceil = min(row - 1, math.ceil(x))
                y_floor = math.floor(y)
                y_ceil = min(col - 1, math.ceil(y))
                u = x - x_floor
                v = y - y_floor
                
                # due to x may not be an integer > we should cast it to an intege
                A = np.matrix([w(1 + u), w(u), w(1 - u), w(2 - u)])
                C = np.matrix([[w(1 + v)], [w(v)], [w(1 - v)], [w(2 - v)]])
                B = np.matrix([
                    [image[int(x_floor) - 1, int(y_floor) - 1][k], image[int(x_floor) - 1, int(y_floor)][k], 
                     image[int(x_floor) - 1, int(y_ceil)][k], image[int(x_floor) - 1, int(y_ceil) + 1][k]],
                    [image[int(x_floor), int(y_floor) - 1][k], image[int(x_floor), int(y_floor)][k], 
                     image[int(x_floor), int(y_ceil)][k], image[int(x_floor), int(y_ceil) + 1][k]],
                    [image[int(x_ceil), int(y_floor) - 1][k], image[int(x_ceil), int(y_floor)][k], 
                     image[int(x_ceil), int(y_ceil)][k], image[int(x_ceil), int(y_ceil) + 1][k]],
                    [image[int(x_ceil) + 1, int(y_floor) - 1][k], image[int(x_ceil) + 1, int(y_floor)][k], 
                     image[int(x_ceil) + 1, int(y_ceil)][k], image[int(x_ceil) + 1, int(y_ceil) + 1][k]]])
                
                result[i, j][k] = np.dot(np.dot(A, B), C)
    return result.astype(np.uint8)


#read the image
img = cv.imread('me.jpg')

#output the result image
pic_1 = bicubic(img, 0.2)
cv.imwrite('bicubic02.jpg', pic_1)

pic_2 = bicubic(img, 5)
cv.imwrite('bicubic5.jpg', pic_2)

pic_3 = bicubic(img, 32)
cv.imwrite('bicubic32.jpg', pic_3)

