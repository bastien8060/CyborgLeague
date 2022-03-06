import time

from ..InterfaceControl import InterfaceControl as Control
from .ShopActions import ActionInstance as Shop
from .PlayerActions import ActionInstance as Player
from .MovementActions import ActionInstance as Movement

class Instance():
    def attackNearbyChampion(self, screen_elements) -> bool:
        champions = screen_elements["champion_points"]
        if len(champions) < 1:
            return False
        champion = champions[0]
        click_x = champion[0]
        click_y = champion[1]

        self.Control.Mouse.click(click_x,click_y)
        return True
    

    def getDistance(self,a,b):
        x1,y1 = a[0],a[1]
        x2,y2 = b[0],b[1]
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def getClosestElement(self,elements):
        distances = []
        center = (0,384)
        for element in elements:
            distances.append(self.getDistance(element,center))
        minIndex = distances.index(min(distances))
        return elements[minIndex]


    def attackAllChampions(self, screen_elements) -> bool:
        champions = screen_elements["champion_points"]

        champion = self.getClosestElement(champions)
        
        click_x = champion[0]
        click_y = champion[1]
        self.Control.Mouse.rightClick(click_x,click_y)
        self.Player.attack("R")
        self.Player.attack("Q")
        self.Player.attack("E")
        self.Player.attack("W")

        time.sleep(0.5)
        return True

    def attackNearbyMinion(self, screen_elements) -> bool:
        minions = screen_elements["minion_points"]
        if len(minions) < 1:
            return False
        minion = self.getClosestElement(minions)
        click_x = minion[0]
        click_y = minion[1]

        self.Control.Mouse.rightClick(click_x,click_y)
        return True

    def followAllMinions(self, screen_elements) -> bool:
        minions = screen_elements["ally_minion_points"]
        if len(minions) < 1:
            return False
        minion = minions[0]
        click_x = minion[0]
        click_y = minion[1]

        self.Control.Mouse.rightClick(click_x,click_y)
        return True

    def attackAllMinions(self, screen_elements) -> bool:
        minions = screen_elements["minion_points"]

        for minion in minions:
            click_x = minion[0]
            click_y = minion[1]
            self.Control.Mouse.rightClick(click_x,click_y)
            time.sleep(0.1)
        return True

    def attackNearbyBuilding(self, screen_elements) -> bool:
        buildings = screen_elements["buildings_points"]
        if len(buildings) < 1:
            return False
        building = buildings[0]
        click_x = building[0]
        click_y = building[1]

        self.Control.Mouse.rightClick(click_x,click_y)
        return True

    def attackAllBuildings(self, screen_elements) -> bool:
        buildings = screen_elements["buildings_points"]

        for building in buildings:
            click_x = building[0]
            click_y = building[1]
            self.Control.Mouse.rightClick(click_x,click_y)
            time.sleep(0.1)
        return True

    def __init__(self) -> None:
        self.Control = Control.Instance()
        self.Shop = Shop()
        self.Player = Player()
        self.Movement = Movement()
