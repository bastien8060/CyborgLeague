import time

from ..InterfaceControl import InterfaceControl as Control


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
    
    def attackAllChampions(self, screen_elements) -> bool:
        champions = screen_elements["champion_points"]
        for champion in champions:
            click_x = champion[0]
            click_y = champion[1]
            self.Control.Mouse.click(click_x,click_y)
            time.sleep(0.5)
        return True

    def attackNearbyMinion(self, screen_elements) -> bool:
        minions = screen_elements["minion_points"]
        if len(minions) < 1:
            return False
        minion = minions[0]
        click_x = minion[0]
        click_y = minion[1]

        self.Control.Mouse.click(click_x,click_y)
        return True

    def attackAllMinions(self, screen_elements) -> bool:
        minions = screen_elements["minion_points"]

        for minion in minions:
            click_x = minion[0]
            click_y = minion[1]
            self.Control.Mouse.click(click_x,click_y)
            time.sleep(0.1)
        return True

    def __init__(self) -> None:
        self.Control = Control.Instance()
