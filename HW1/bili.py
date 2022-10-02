import cv2 as cv
import numpy as np
import math

#imple Bilinear Interpolation
def bilinear(image, scaling_factor):
    row, col, dim = image.shape
    new_row = int(row * scaling_factor)
    new_col = int(col * scaling_factor)
    # create new image
    result = np.zeros((new_row, new_col, dim))
    
    # mapping to origin image
    for i in range(new_row):
        for j in range(new_col):
            x = i / scaling_factor
            y = j / scaling_factor
            
            #計算要 Bilinear Interpolation 的四條線
            x_floor = math.floor(x)
            x_ceil = min(row - 1, math.ceil(x))
            y_floor = math.floor(y)
            y_ceil = min(col - 1, math.ceil(y))
            
            #利用上述四條線獲得四周的端點
            top_left = image[x_floor, y_floor, : ]
            top_right = image[x_floor, y_ceil, : ]
            down_left = image[x_ceil, y_floor, : ]
            down_right = image[x_ceil, y_ceil, : ]
            
            # due to x & y may not be an integer > we should cast it to an integer thus we use(int)x
            if (x_ceil == x_floor) and (y_ceil == y_floor):
                q = image[int(x), int(y), :]
            elif (x_ceil == x_floor):
                q1 = image[int(x), int(y_floor), :]
                q2 = image[int(x), int(y_ceil), :]
                q = q1 * (y_ceil - x) + q2 * (y - x_floor)  
            elif (y_ceil == y_floor):
                q1 = image[int(x_floor), int(y), :]
                q2 = image[int(x_ceil), int(y), :]
                q = (q1 * (x_ceil - y)) + (q2 * (x - y_floor))
            else:
                q1 = top_left * (y_ceil - y) + top_right * (y - y_floor)
                q2 = down_left * (y_ceil - y) + down_right * (y - y_floor)
                q = q1 * (x_ceil - x) + q2 * (x - x_floor)
                
            result[i, j, :] = q # assign result to the result image
    return result.astype(np.uint8)

#read the image
img = cv.imread('me.jpg')

#output the result image
pic_1 = bilinear(img, 0.2)
cv.imwrite('bilinear_02.jpg', pic_1)


pic_2 = bilinear(img, 5)
cv.imwrite('bilinear5.jpg', pic_2)


pic_3 = bilinear(img, 32)
cv.imwrite('bilinear32.jpg', pic_3)

