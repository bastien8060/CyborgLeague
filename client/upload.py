import os
import requests
import time

from PIL import Image
import io

def resize(filename):
    img1 = Image.open(filename)

    print(img1.size)

    im1_resize = img1.resize((img1.size[0]//2, img1.size[1]//2), Image.ANTIALIAS)

    with io.BytesIO() as output:
        im1_resize.save(output, 'png')
        return output.getvalue()



start = time.time()
path_img = 'output.jpg'
url = "http://163.172.97.55:44444"

img = resize(path_img)
# Requests makes it simple to upload Multipart-encoded files 
files = {'media': img}
requests.post(url, files=files)
print("Process time:", (time.time() - start))