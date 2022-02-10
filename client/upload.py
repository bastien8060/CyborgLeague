import os
import requests
import time

from PIL import Image
import io

def resize(filename):
    img1 = Image.open(filename)
    #print(img1.size)
    #img1 = img1.resize((img1.size[0]//2, img1.size[1]//2), Image.ANTIALIAS)
    with io.BytesIO() as output:
        img1.save(output, 'png')
        return output.getvalue()



start = time.time()
path_img = 'output.jpg'
url = "http://127.0.0.1:44444"

img = open(path_img,"rb")
# Requests makes it simple to upload Multipart-encoded files 
requests.post(url, files={'media': img})
img.close()
print("Process time:", (time.time() - start))