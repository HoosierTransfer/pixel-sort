import cv2
import os
import numpy as np

windowName = "sort"

filename_with_ext = "hqdefault.jpg"

filename, ext = os.path.splitext(filename_with_ext)

# val1 = 56
# val2 = 182

val1 = 255*0.3
val2 = 255*0.8

def get_sequential_255_indices(arr):
    indices = np.where(arr == 255)[0]

    diff = np.diff(indices)
    split_indices = np.where(diff > 1)[0]

    sequential_indices = np.split(indices, split_indices + 1)

    return sequential_indices

image = cv2.imread(filename_with_ext)

im = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]

im_sort_channel = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 0]


mask = cv2.inRange(im, val1, val2)

for i in range(len(im)):
    ones = get_sequential_255_indices(mask[i])
    for j in range(len(ones)):
        if len(ones[j]) == 0:
            continue
        sorted_indices = np.argsort(im_sort_channel[i][ones[j][0]:ones[j][-1] + 1])
        image[i][ones[j][0]:ones[j][-1] + 1] = image[i][ones[j][0]:ones[j][-1] + 1][sorted_indices]

cv2.imwrite(filename + "_sorted.png", image)
cv2.imwrite(filename + "_mask.png", mask)




# def on_change(_):
#     lower_value = cv2.getTrackbarPos('low', windowName)
#     upper_value = cv2.getTrackbarPos('high', windowName)
#     im = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[..., 2]

#     thresholded = cv2.inRange(im, lower_value, upper_value)
#     cv2.imshow(windowName, thresholded)


# cv2.imshow(windowName, mask)

# cv2.createTrackbar('low', windowName, 0, 255, on_change)
# cv2.createTrackbar('high', windowName, 0, 255, on_change)

# cv2.waitKey(0)
# cv2.destroyAllWindows()