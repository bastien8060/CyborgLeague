import time
from .VisionApi import VisionApi

Vision = VisionApi.Instance()

class CyborgLeagueBot:
    def __init__(self):
        self.running = False

async def start():
    bot.running = True
    while bot.running:
        if Vision.isReady():
            if Vision.cooldown:
                time.sleep(0.5)
                Vision.cooldown = False
            img = Vision.screenshot()
            Vision.upload(img)
        else:
            Vision.cooldown = True
            time.sleep(0.01)

bot = CyborgLeagueBot()

