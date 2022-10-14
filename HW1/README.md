## Digital Image Process<br>

### Bilinear interpolation<br>
reference:<br>
`https://en.wikipedia.org/wiki/Bilinear_interpolation`<br>
根據維基百科<br>
我實作了 Bilinear interpolation 的 funtion 如下<br>
```
#implement Bilinear Interpolation
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
```
### Bicubic interpolation<br>
根據維基百科<br>
我實作了 Bicubic interpolation 的 funtion 如下<br>
```
def w(x, a = -0.5):
    if abs(x) <= 1:
        return (a + 2) * (abs(x) ** 3) - (a + 3) * (abs(x) ** 2) + 1 
    elif abs(x) > 1 and abs(x) < 2:
        return a * (abs(x) ** 3) - (5 * a) * (abs(x) ** 2) + 8 * a * abs(x) - 4 * a
    else:
        return 0
def pad_around(image):
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
    image = pad_around(image)
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
```

reference:<br>
`https://en.wikipedia.org/wiki/Bicubic_interpolation`<br>
`https://www.twblogs.net/a/5ee5256006527f2d10e1b6e9`<br>

### Faster way <br>
做完之後發現其實 OpenCv 有提供一個方便的函數供我們使用<br>
這個函數的名字是 `resize()`<br>
關於裡面的參數有興趣可以到官網上查詢<br>

### Comparison
我把透過自己手刻的函式以及藉由Opencv提供的函式所產生的結果<br>
放在不同的資料夾，以提供比較<br>
不過直接呼叫函式時間上快多了ＸＤＤ<br>



