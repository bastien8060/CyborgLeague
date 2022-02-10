# pylint: skip-file
#!/usr/env python3
import http.server
import socketserver
import io
import cgi
import cv2, time, sys
import numpy as np
import time



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
            __image = cv2.rectangle(__image,(max_loc[0]+25,max_loc[1]+50), (max_loc[0]+w+1+25, max_loc[1]+h+1+50), __style[0], __style[1] )
    return __image



def searchall(image):
    start = time.time()

    image = search(image,building_1,0.91,[(0,0,255),4])
    image = search(image,building_2,0.91,[(0,0,255),4])
    image = search(image,building_3,0.91,[(0,0,255),4])
    image = search(image,turret,0.91,[(0,0,255),4])
    image = search(image,minion,0.93,[(0,255,0),4])
    image = search(image,champion_1,0.80,[(255,0,255),4])
    image = search(image,champion_2,0.85,[(255,0,0),4])

    cv2.imwrite('output.png',image)

    print("Process time:", (time.time() - start))



class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):        
        r, info = self.deal_post_data()
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()      

    def deal_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            print (type(form))
            try:
                if isinstance(form["media"], list):
                    for record in form["media"]:
                        buf =  record.file.read()
                        #use numpy to construct an array from the bytes
                        x = np.fromstring(buf, dtype='uint8')
                        #decode the array into an image
                        img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
                        searchall(img)
                else:
                    buf = form["media"].file.read()
                    #use numpy to construct an array from the bytes
                    x = np.fromstring(buf, dtype='uint8')
                    #decode the array into an image
                    img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
                    searchall(img)
                    
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
        return (True, "Files uploaded")






def resize(src):
    height, width = src.shape[:2]
    return cv2.resize(src, (0,0), fx=0.5, fy=0.5) 





method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
turret = resize(cv2.imread('training_data/img/patterns/units/turret.png'))
minion = resize(cv2.imread('training_data/img/patterns/units/minion.png'))
champion_1 = resize(cv2.imread('training_data/img/patterns/units/champion.png'))
champion_2 = resize(cv2.imread('training_data/img/patterns/units/champion_2.png'))
building_1 = resize(cv2.imread('training_data/img/patterns/units/building_1.png'))
building_2 = resize(cv2.imread('training_data/img/patterns/units/building_2.png'))
building_3 = resize(cv2.imread('training_data/img/patterns/units/building_3.jpg'))




# Change this to serve on a different port
PORT = 44444

Handler = CustomHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()



