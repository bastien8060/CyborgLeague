import time
import multiprocessing

class Instance():

    def deamon(self) -> multiprocessing.Process:
        """
        Deamon/Background Process to run update the API stats automatically.
        """
        mProcess = multiprocessing.Process(target=self.reload)
        return mProcess
    
    def autoreload(self):
        while True:
            self.reload()
            time.sleep(0.01)

    def reload(self) -> bool:
        self.stats = self.Slaw.get_live("/liveclientdata/activeplayer")
        return True

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

    def getRatioHP(self) -> float:
        s = self.stats["championStats"]
        return float(s["currentHealth"]/s["maxHealth"])
    
    def getGold(self) -> float:
        return float(self.stats["currentGold"])

    def isDead(self) -> bool:
        return int(self.getHP()) == 0

    def getLevel(self) -> int:
        return int(self.stats["level"])

    def __init__(self,Slaw) -> None:
        self.Slaw = Slaw
        return