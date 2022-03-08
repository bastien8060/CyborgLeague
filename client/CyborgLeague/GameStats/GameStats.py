import time
import multiprocessing

class Instance():

    def deamon(self) -> multiprocessing.Process:
        """
        Deamon/Background Process to run update the API stats automatically.
        """
        multiprocessing.freeze_support()
        mProcess = multiprocessing.Process(target=self.reload)
        return mProcess
    
    def autoreload(self):
        while True:
            self.reload()
            time.sleep(0.1)

    def reload(self) -> bool:
        if self.previous_stats != None:
            self.previous_stats = self.stats
        else:
            self.previous_stats = self.Slaw.get_live("/liveclientdata/allgamedata")["activePlayer"]
            self.previous_stats["level"] = 0
        self.stats = self.Slaw.get_live("/liveclientdata/allgamedata")["activePlayer"]
        self.gamestats = self.Slaw.get_live("/liveclientdata/gamestats")
        self.events = self.Slaw.get_live("/liveclientdata/eventdata")["Events"]
        return True

    def getEvents(self):
        return self.events

    def getDataReload(self):
        return (self.stats,self.previous_stats)

    def getChampionName(self):
        return self.stats["summonerName"]

    def getGameTime(self) -> float:
        return float(self.gamestats["gameTime"])

    def died(self):
        self.wasDead = True
        return True

    def revived(self):
        condition = self.wasDead
        self.wasDead = False
        return condition

    def isTakingDamage(self) -> bool:
        old = self.previous_stats["championStats"]
        return (float(old["currentHealth"]) - self.getHP()) > 80

    def isHalfLife(self) -> bool:
        return self.getHP() < (self.getMaxHP() * 0.6)

    def isLowLife(self) -> bool:
        return self.getHP() < (self.getMaxHP() * 0.4)

    def isRich(self) -> bool:
        return self.getGold() > 2100

    def needsEnergy(self) -> bool:
        s = self.stats["championStats"]
        if "resourceValue" not in s:
            return False
        if "resourceMax" not in s:
            return False
        if int(s["resourceMax"]) == 0:
            return False
        return True

    def getEnergy(self) -> float:
        if not self.needsEnergy():
            return float(10000)
        s = self.stats["championStats"]
        return float(s["resourceValue"])

    def getRatioEnergy(self) -> float:
        if not self.needsEnergy():
            return float(1)
        s = self.stats["championStats"]
        return float(s["resourceValue"]/s["resourceMax"])
    
    def getHP(self) -> float:
        s = self.stats["championStats"]
        return float(s["currentHealth"])
    
    def getMaxHP(self) -> float:
        s = self.stats["championStats"]
        return float(s["maxHealth"])

    def getRatioHP(self) -> float:
        s = self.stats["championStats"]
        return float(s["currentHealth"]/s["maxHealth"])
    
    def getGold(self) -> float:
        return float(self.stats["currentGold"])

    def isDead(self) -> bool:
        return int(self.getHP()) == 0

    def getLevel(self) -> int:
        return int(self.stats["level"])

    def getAbilitiesLvl(self) -> dict:
        keys = ["Q","W","E","R"]
        abilities = dict.fromkeys(keys, 0)
        for key in keys:
            lvl = self.stats["abilities"][key]["abilityLevel"]
            abilities[key] = lvl
        return abilities

    def hasLeveledUp(self) -> bool:
        return self.previous_stats["level"] != self.stats["level"]

    def didBuyStarterPack(self) -> bool:
        return self.hasBoughtStarterPack

    def boughtStarterPack(self):
        self.hasBoughtStarterPack = True

    def init(self, Slaw) -> bool:
        self.Slaw = Slaw
        return True

    def __init__(self) -> None:
        self.stats = None
        self.previous_stats = self.stats
        self.hasBoughtStarterPack = False
        return