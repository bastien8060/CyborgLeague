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
            img = Vision.screenshot()
            Vision.upload(img)
        else:
            time.sleep(0.01)

bot = CyborgLeagueBot()

