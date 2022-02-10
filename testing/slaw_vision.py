# pylint: skip-file
import sys
import time
import cv2
import numpy as np
import win32con
import win32gui
import win32ui
from mss import mss
from win32api import GetSystemMetrics
from win32gui import GetForegroundWindow, GetWindowText

sct = mss()
monitor_1 = sct.monitors[0]


bounding_box = {
            "top": 0,
            "left": 0,
            "width": 1920,
            "height": 1080,
        },

def screenshot():
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)

    sct_original = np.asarray(sct.grab(monitor_1))
    sct_img = cv2.cvtColor(sct_original, cv2.COLOR_BGRA2BGR)
    return sct_img

    

def search(__image,__template,__threshold,__style):
    h, w = __template.shape[:2]

    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(__image, __template, method)

    # fake out max_val for first run through loop
    max_val = 1
    prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = None, None, None, None
    while max_val > __threshold:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        # Prevent infinite loop. If those 4 values are the same as previous ones, break the loop.
        if prev_min_val == min_val and prev_max_val == max_val and prev_min_loc == min_loc and prev_max_loc == max_loc:
            break
        else:
            prev_min_val, prev_max_val, prev_min_loc, prev_max_loc = min_val, max_val, min_loc, max_loc
        
        if max_val > __threshold:
            # Prevent start_row, end_row, start_col, end_col be out of range of image
            start_row = max_loc[1] - h // 2 if max_loc[1] - h // 2 >= 0 else 0
            end_row = max_loc[1] + h // 2 + 1 if max_loc[1] + h // 2 + 1 <= res.shape[0] else res.shape[0]
            start_col = max_loc[0] - w // 2 if max_loc[0] - w // 2 >= 0 else 0
            end_col = max_loc[0] + w // 2 + 1 if max_loc[0] + w // 2 + 1 <= res.shape[1] else res.shape[0]

            res[start_row: end_row, start_col: end_col] = 0
            #__image = cv2.rectangle(__image,(max_loc[0]+25,max_loc[1]+50), (max_loc[0]+w+1+25, max_loc[1]+h+1+50), __style[0], __style[1] )
    return __image


method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
turret = cv2.imread('training_data/img/patterns/units/turret.png')
minion = cv2.imread('training_data/img/patterns/units/minion.png')
champion_1 = cv2.imread('training_data/img/patterns/units/champion.png')
champion_2 = cv2.imread('training_data/img/patterns/units/champion_2.png')
building_1 = cv2.imread('training_data/img/patterns/units/building_1.png')
building_2 = cv2.imread('training_data/img/patterns/units/building_2.png')
building_3 = cv2.imread('training_data/img/patterns/units/building_3.jpg')

start = time.time()
print("now")
for i in range(3):
    image = screenshot()

    image = search(image,building_1,0.91,[(0,0,255),4])
    image = search(image,building_2,0.91,[(0,0,255),4])
    image = search(image,building_3,0.91,[(0,0,255),4])
    image = search(image,turret,0.91,[(0,0,255),4])
    image = search(image,minion,0.93,[(0,255,0),4])
    image = search(image,champion_1,0.80,[(255,0,255),4])
    image = search(image,champion_2,0.85,[(255,0,0),4])
 
print("Process time:", (time.time() - start))



#cv2.imwrite('output.jpg',image)
# The image is only displayed if we call this
cv2.imshow('output',image)
cv2.waitKey(0)



