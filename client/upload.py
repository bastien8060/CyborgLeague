import os
import requests
import time

from PIL import Image
import io
import cv2

def resize(filename):
    src = cv2.imread(filename)
    
    height, width = src.shape[:2]
    src = cv2.resize(src, (0,0), fx=0.5, fy=0.5) 

    with io.BytesIO() as output:
        cv2.imwrite("output.png", src)
        return output.getvalue()



start = time.time()
path_img = 'output.jpg'
url = "http://163.172.97.55:44444"

img = resize(path_img)
# Requests makes it simple to upload Multipart-encoded files 
files = {'media': img}
requests.post(url, files=files)
print("Process time:", (time.time() - start))