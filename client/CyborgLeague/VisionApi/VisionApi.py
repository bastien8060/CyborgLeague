import io
import json
import sys
import os
import time

import cv2
import numpy as np
import requests
if os.name == 'nt':
    import win32con
    import win32gui
    import win32ui
    from mss import mss
    from win32api import GetSystemMetrics
    from win32gui import GetForegroundWindow, GetWindowText
else:
    raise Exception("Client only supports Windows")


class Instance:
    def upload(self,img):    
        start_upload = time.time()

        is_success, buffer = cv2.imencode(".jpg", img)
        img = io.BytesIO(buffer)

        request = requests.post(self.backend_url, files={'media': img})
        
        return (time.time() - start_upload),json.loads(request.content)

    def isReady(self) -> bool:
        return GetWindowText(GetForegroundWindow()) == "League of Legends (TM) Client"

    def screenshot(self):
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)

        sct_original = np.asarray(self.__sct.grab(self.__monitor_1))
        sct_img = cv2.cvtColor(sct_original, cv2.COLOR_BGRA2BGR)
        return sct_img

    def runhook(self,result):
        champions = result["champion_points"]
        minions = result["minion_points"]
        buildings = result["buildings_points"]

        print(f"Champions: {len(champions)}")
        print(f"Minions: {len(minions)}")
        print(f"Buildings: {len(buildings)}")


    def __init__(self, url="http://127.0.0.1:44444"):
        self.cooldown = True
        self.backend_url = url
        self.__sct = mss()
        self.__monitor_1 = self.__sct.monitors[0]

        self.__bounding_box = {
                    "top": 0,
                    "left": 0,
                    "width": 1920,
                    "height": 1080,
                },

