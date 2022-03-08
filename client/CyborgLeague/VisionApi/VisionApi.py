import io
import json
import os
import sys
import time

import cv2
import numpy as np
import requests

if os.name == 'nt':
    import pywintypes
    from mss import mss
    from win32api import GetSystemMetrics
    from win32gui import GetForegroundWindow, GetWindowText
else:
    raise Exception("Client only supports Windows")




class Instance:
    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        print(dim) 

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

        
    def upload(self,img,champions=[]):    
        start_upload = time.time()

        is_success, buffer = cv2.imencode(".jpg", img)
        img = io.BytesIO(buffer)


        data = {"champions":json.dumps(champions)}
        files = {'media': img}
        request = requests.post(self.backend_url+"/api/v1/upload", data=data, files=files)
        
        print(time.time() - start_upload)
        return (time.time() - start_upload),json.loads(request.content)

    def isReady(self) -> bool:
        return GetWindowText(GetForegroundWindow()) == "League of Legends (TM) Client"

    def screenshot(self,debug=False):
        w = GetSystemMetrics(0)
        h = GetSystemMetrics(1)
        
        screenshot = self.__sct.grab(self.__monitor_1)

        #if debug:
        #    mss.tools.to_png(screenshot.rgb, screenshot.size, output="output.png")

        sct_original = np.asarray(screenshot)
        sct_img = cv2.cvtColor(sct_original, cv2.COLOR_BGRA2BGR)
        resized = sct_img[0:768, 0:1366]

        if debug:
            cv2.imwrite("output.png",resized)

        return resized

    def runhook(self,result):
        champions = result["champion_points"]
        minions = result["minion_points"]
        buildings = result["buildings_points"]
        ally_champions = result["ally_champion_points"]
        ally_buildings = result["ally_buildings_points"]
        ally_minion = result["ally_minion_points"]

        print(f"Champions: {len(champions)}")
        print(f"Minions: {len(minions)}")
        print(f"Buildings: {len(buildings)}")

        print(f"Ally Minions: {len(ally_minion)}")
        print(f"Ally Champions: {len(ally_champions)}")
        print(f"Ally Buildings: {len(ally_buildings)}")


    def init(self,url):
        self.backend_url = url

    def __init__(self):
        self.cooldown = True
        self.__sct = mss()
        self.__monitor_1 = self.__sct.monitors[0]

        self.__bounding_box = {
                    "top": 0,
                    "left": 0,
                    "width": 1920,
                    "height": 1080,
                    "mon":0
                },

