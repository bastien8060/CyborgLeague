from ..InterfaceControl import InterfaceControl as Control

class minimapZone():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.trueX = x + int(1366/1.2532)
        self.trueY = y + int(768/1.5578)

class minimapLocator():
    def getClosestTurret(self,playerZone:minimapZone):
        distances = []
        turrets = []
        for turret in self.turrets:
            if not turret["status"]:
                continue
            location = turret["location"]
            name = turret["name"]
            distance = self.getDistance(location,playerZone)
            distances.append(distance)
            turrets.append(turret)

        minIndex = distances.index(min(distances))
        return turrets[minIndex]

    def getTurretByName(self,name):
        for turret in self.turrets:
            if name == turret["name"]:
                return turret
        return False

    def getDistance(self,a:minimapZone,b:minimapZone):
        x1,y1 = a.x,a.y
        x2,y2 = b.x,b.y
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


    def parseEvents(self,events):
        for event in events:
            if event["EventName"] != "TurretKilled":
                continue
            turret = event["TurretKilled"]
            for name in self.turrets:
                if name["name"] == turret:
                    name["status"] = False

    def __init__(self) -> None: 
        self.turrets = [
            {"name":"Turret_T2_L_03_A","location":minimapZone(13,78),"status":True},
            {"name":"Turret_T2_C_05_A","location":minimapZone(100,152),"status":True},
            {"name":"Turret_T2_R_03_A","location":minimapZone(183,240),"status":True},
            {"name":"Turret_T2_L_02_A","location":minimapZone(22,143),"status":True},
            {"name":"Turret_T2_C_04_A","location":minimapZone(84,178),"status":True},
            {"name":"Turret_T2_R_02_A","location":minimapZone(116,236),"status":True},
            {"name":"Turret_T2_L_01_A","location":minimapZone(16,189),"status":True},
            {"name":"Turret_T2_C_03_A","location":minimapZone(55,200),"status":True},
            {"name":"Turret_T2_R_01_A","location":minimapZone(67,237),"status":True},
            {"name":"Turret_T2_C_02_A","location":minimapZone(28,221),"status":True},
            {"name":"Turret_T2_C_01_A","location":minimapZone(31,226),"status":True},
            {"name":"Player_Ally_Base","location":minimapZone(13,239),"status":True}
        ]



class ActionInstance:
    def __init__(self) -> None:
        self.minimapGuide = minimapLocator()
        self.Control = Control.Instance()
        self.minimap = []
        return

    def createMinimapZone(self,x,y):
        return minimapZone(x,y)

    def fallback(self,zone:minimapZone) -> bool:
        turret = self.minimapGuide.getClosestTurret(zone)
        self.clickOnMinimap(turret["location"])

    def update(self,screen,events):
        self.minimap = screen["minimap"]
        self.minimapGuide.parseEvents(events)
    
    def clickOnMinimap(self,zone:minimapZone) -> bool:
        x,y = zone.trueX,zone.trueY
        self.Control.Mouse.rightClick(x,y)
        self.Control.Mouse.resetMouse()
        return True

    

