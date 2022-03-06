# pylint: skip-file
#!/usr/env python3
import cv2
import numpy as np
import time
import requests

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class PointsCollection:
    def __init__(self):
        return

def CoordinateCorrector(xy,name):
    if name.startswith("hero_"):
        return xy
    name = name.replace("ally_","")
    """Corrects the coordinates from the health bar to the actual location to click the element.\n
    Eg. Corrects the coordinates from a minion's healthbar to the actual position of the minion."""
    xy[0] += {
        'minion_points': 5,
        'champion_points': 20,
        'buildings_points': 20,
    }[name]
    xy[1] += {
        'minion_points': 10,
        'champion_points': 80,
        'buildings_points': 0,
    }[name]
    return xy


def minimap_analysis(_img, champions):
    championPoints = []

    width, height = _img.shape[1::-1]
    x1, x2 = int(width/1.2532), int(width/1.0088)
    y1, y2 = int(height/1.5578), int(height/1.0172)

    match_method = cv2.TM_SQDIFF_NORMED
    img = _img.copy()[y1:y2,x1:x2]

    for champion in champions:

        template = points.champions[champion]

        scale = 1.1

        tmpl = cv2.resize(template, (0,0),fx = scale, fy=scale)

        result = cv2.matchTemplate(img, tmpl, match_method)

        _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)

        matchLoc = minLoc #maxLoc if not cv.TM_SQDIFF or cv.TM_SQDIFF_NORMED
        # here perhaps try to normalize the results?
        #endLoc = (matchLoc[0] + tmpl.shape[1],matchLoc[1] + tmpl.shape[0])

        AverageLoc = int((matchLoc[0]*2 + tmpl.shape[1])/2),int((matchLoc[1]*2 + tmpl.shape[0])/2)

        #cv2.rectangle(img, matchLoc, endLoc, (0,0,255), 1)
        #cv2.imwrite(f"debug/debug_{scale}.png",img)
        if _minVal < 0.3:
            championPoints.append({"champion":champion,"location":AverageLoc,"p":_minVal})

    return json.dumps(championPoints)






def findColor(point,__image):
    x1, y1 = int(point[0]) - 0, int(point[1]) - 2
    x2, y2 = int(point[0]) + 10, int(point[1]) + 2
    sample = __image[y1:y2, x1:x2]

    avg = sample.mean(axis=0).mean(axis=0)

    r,g,b = int(avg[2]),int(avg[1]),int(avg[0])

    if r > g and r > b:
        return 0
    return 1


def search(__color_image,__template,__threshold,name,queue):
    #print(f"starting {name}")
    allyPoints = []
    enemyPoints = []
    h, w = __template.shape[:2]

    method = cv2.TM_CCOEFF_NORMED #try sqdiff and without normed

    __image = cv2.cvtColor(__color_image, cv2.COLOR_BGR2GRAY)

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
            averageXPoint = (max_loc[0]+max_loc[0]+w+51)/2
            averageYPoint = (max_loc[1]+max_loc[1]+h+101)/2

            color = findColor([(max_loc[0]+max_loc[0]+w)/2,(max_loc[1]+max_loc[1]+h)/2],__color_image)
            
            alt_name = "ally_"+name if color else name

            averagePoint = CoordinateCorrector([averageXPoint,averageYPoint],alt_name)
            
            allyPoints.append(averagePoint) if color else enemyPoints.append(averagePoint)
          
    queue.put({"name":name,"points":enemyPoints})
    queue.put({"name":"ally_"+name,"points":allyPoints})
    return



def searchall(image):
    """
    Simple multi-thread implementation with CV2 to search simulataneously for multiple templates. \n
    Uses python's multiprocessing. Only recommended on Linux, as windows lack of support in forking processes, makes this feature a bottleneck.\n
    Support on MacOS varies and may surprise some, as it is known to be buggy (Try with caution/not for the fainthearted).
    """

    queue = SimpleQueue()

    turret_process = Process(target=search, args=(image,points.building_1,0.91,"buildings_points", queue))
    building2_process = Process(target=search, args=(image,points.building_2,0.91,"buildings_points", queue))
    minion_process = Process(target=search, args=(image,points.minion,0.96, "minion_points", queue))
    champion_process = Process(target=search, args=(image,points.ally_champion_1,0.88, "champion_points", queue))

    #champion_process = Process(target=search, args=(image,points.champion_1,0.98, "champion_points", queue))
    #ally_minion_process = Process(target=search, args=(image,points.ally_minion,0.95, "ally_minion_points", queue))
    #ally_turret_process = Process(target=search, args=(image,points.ally_building_1,0.91,"ally_buildings_points", queue))
    #ally_building2_process = Process(target=search, args=(image,points.ally_building_2,0.91,"ally_buildings_points", queue))
    #ally_champion2_process = Process(target=search, args=(image,points.ally_champion_2,0.88,[(255,0,255),4], "ally_champion_points", queue))

    minion_process.start()
    turret_process.start()
    building2_process.start()
    champion_process.start()

    minion_process.join()
    turret_process.join()
    building2_process.join()
    champion_process.join()

    all_points = {}
    
    # Merges together all async results into a single dict, using the queue we set earlier.
    # `all_points = {name: *name*,"points": [(x,y), (x,y), ...] }`
    print("[*] Sorting async queue")
    for _ in range(8):
        v = queue.get()
        #print(v)
        name = v["name"]
        if name in all_points:
            all_points[name].extend(v["points"])
        else:
            all_points[name] = v["points"]
    return all_points

def screen_analysis(img):
    print("[*] Starting Async Threads: 8")
    points = searchall(img)

    return points


@app.route("/", methods=['GET'])
def home():
    return "CyborgLeague OpenCV Server"

@app.route("/api/v1/upload", methods=['GET', 'POST'])
def handle_upload():
    champions = json.loads(request.values['champions'])

    uploaded_file = request.files['media']
    if uploaded_file.filename != '':
        start = time.time()
        stream = uploaded_file.stream.read()
        x = np.fromstring(stream, dtype='uint8')
        img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
        minimap = minimap_analysis(img,champions)
        screen = screen_analysis(img)
        screen["minimap"] = minimap
        print(f"Process time: {(time.time() - start)}"+"\n")

        return json.dumps(screen)
    return "error"

def main():
    global points
    method = cv2.TM_SQDIFF_NORMED

    points = PointsCollection()

    # Read the images from the file
    points.minion = cv2.cvtColor(cv2.imread('patterns/minion.png'), cv2.COLOR_BGR2GRAY)
    points.champion_1 = cv2.cvtColor(cv2.imread('patterns/champion.png'), cv2.COLOR_BGR2GRAY)
    points.building_1 = cv2.cvtColor(cv2.imread('patterns/building_1.png'), cv2.COLOR_BGR2GRAY)
    points.building_2 = cv2.cvtColor(cv2.imread('patterns/building_2.png'), cv2.COLOR_BGR2GRAY)
    points.ally_minion = cv2.cvtColor(cv2.imread('patterns/ally_minion.png'), cv2.COLOR_BGR2GRAY)
    points.ally_champion_1 = cv2.cvtColor(cv2.imread('patterns/ally_champion.png'), cv2.COLOR_BGR2GRAY)
    #points.ally_champion_2 = cv2.imread('patterns/ally_champion_2.png')
    points.ally_building_1 = cv2.cvtColor(cv2.imread('patterns/ally_building_1.png'), cv2.COLOR_BGR2GRAY)
    points.ally_building_2 = cv2.cvtColor(cv2.imread('patterns/ally_building_2.png'), cv2.COLOR_BGR2GRAY)

    points.champions = {}


    request = requests.get("https://raw.githubusercontent.com/ngryman/lol-champions/master/champions.json")
    characters = json.loads(request.content.decode())

    for character in characters:
        champion = character["name"].replace(" ","").replace("'","").replace(".","")
        points.champions[champion] = cv2.imread(f'patterns/champions_16x16/{champion}.png')

    bjoern.run(app, "0.0.0.0", 39743)


if __name__ == "__main__":
    import json
    from multiprocessing import Process, SimpleQueue
    import bjoern

    main()

