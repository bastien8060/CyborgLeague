import io
import sys
import time

import cv2
import numpy as np
import requests
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


def upload(img):    
    start_upload = time.time()
    url = "http://127.0.0.1:44444"

    is_success, buffer = cv2.imencode(".jpg", img)
    img = io.BytesIO(buffer)
    # Requests makes it simple to upload Multipart-encoded files 
    requests.post(url, files={'media': img})
    print("Upload time:", (time.time() - start_upload))

def screenshot():
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)

    sct_original = np.asarray(sct.grab(monitor_1))
    sct_img = cv2.cvtColor(sct_original, cv2.COLOR_BGRA2BGR)
    return sct_img


