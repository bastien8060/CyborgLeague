import requests

from ..InterfaceControl import InterfaceControl as Control

class OptimalStats():
    def __init__(self):
        return
    
    def skillOrder(self,playerName):
        return ["Q","E","W","E","E","R","E","W","E","W","R","W","W","Q","Q","R","Q","Q"]

class ActionInstance:
    def __init__(self,) -> None:
        self.Control = Control.Instance()
        self.OptStats = OptimalStats()
        return

    def levelUpAbility(self,playerLevel,playerName):
        ability = self.OptStats.skillOrder(playerName)[playerLevel - 1]
        self.Control.Keyboard.hold_key("KEY_LCONTROL",_calledDirectly=True)
        self.Control.Keyboard.press_key(f"KEY_{ability}",duration=50)
        self.Control.Keyboard.release_key("KEY_LCONTROL",_calledDirectly=True)

    def attack(self,attackSlot):
        self.Control.Keyboard.press_key(f"KEY_{attackSlot}",duration=40)

    def useItemSlot(self,slot):
        self.Control.Keyboard.press_key(f"KEY_{slot}",duration=50)

        
    def useSummonerSpell(self,slot):
        """
        Abilities key/slot: 
        - (1) D Spell
        - (2) F Spell
        - (3) B (Recall to base)
        """
        spell = ["D","F","B"][slot-1]
        self.Control.Keyboard.press_key(f"KEY_{spell}",duration=50)