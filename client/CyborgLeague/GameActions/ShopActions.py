import json
import time

import requests
from flask import request

from ..InterfaceControl import InterfaceControl as Control


class ActionInstance:
    def __init__(self) -> None:
        self.Control = Control.Instance()
        self.shopInventory = {}
        self.update()
        self.owned = {}
        self.wallet = 0
        return
    
    def buildNextRecommended(self):
        items = ["3006","6673","3508","6675","3046","3031"]
        for item in items:
            if self.isOwned(item):
                continue
            self.build_item(item)
            return


    def update(self,wallet=0):
        patch_version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        patch_version = json.loads(patch_version.content.decode())[0]

        shopInventory = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/data/en_US/item.json")
        self.updateWallet(wallet)
        self.shopInventory = json.loads(shopInventory.content.decode())["data"]

    def updateWallet(self,wallet):
        self.wallet = wallet

    def areOwned(self, items:list):
        return  all(item in self.owned for item in items)

    def isOwned(self, item):
        if item not in self.owned:
            return 0
        else:
            return self.owned[item]

    def AddOwned(self,item):
        if item not in self.owned:
            self.owned[item] = 1
        else:
            self.owned[item] += 1
    
    def RemoveOwned(self,item):
        if item not in self.owned:
            print("[*] Error Item not owned in DICT")
        else:
            if self.owned[item] == 1:
                self.owned.pop(item, None)
            else:
                self.owned[item] -= 1

    def toggle(self):
        self.Control.Keyboard.press_key("KEY_P")
        time.sleep(1)

    def buy(self,item,base=False,wallet=-1) -> bool:
        if wallet:
            self.updateWallet(wallet)

        name = self.shopInventory[item]["name"]
        if base:
            price = self.shopInventory[item]["gold"]["base"]
        else:
            price = self.shopInventory[item]["gold"]["total"]
        fancyName = self.shopInventory[item]["name"]
        self.AddOwned(item)
        self.wallet -= price

        time.sleep(0.5)
        self.Control.Keyboard.hold_key("KEY_LCONTROL")
        time.sleep(0.1)
        self.Control.Keyboard.press_key("KEY_L",duration=500)
        time.sleep(0.1)
        self.Control.Keyboard.release_key("KEY_LCONTROL")
        time.sleep(2)

        self.Control.Keyboard.type_text(name,duration=100)
        time.sleep(0.1)

        self.Control.Keyboard.press_key("KEY_RETURN")

        print(f"Bought {fancyName} for {price}")

    def build_item(self,item:str) -> bool:
        infoItem = self.shopInventory[item]
        base_price = infoItem["gold"]["base"]
        price = infoItem["gold"]["total"]

        if self.isOwned(item):
            return True
        if price-5 <= self.wallet:
            return self.buy(item)
        if "from" not in infoItem:
            return False
        baseItems = infoItem["from"]

        if not self.areOwned(baseItems):
            for subitem in baseItems:
                if not self.isOwned(subitem):
                    self.build_item(subitem)

        if self.areOwned(baseItems):
            if base_price <= self.wallet:
                return self.buy(item,base=True)

        return False
        


        
