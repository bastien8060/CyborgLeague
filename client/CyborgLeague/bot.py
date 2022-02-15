import os
import time

from .GameActions import GameActions as Actions
from .VisionApi import VisionApi

if os.name == 'nt':
    from win32api import GetKeyState
    from win32con import VK_CAPITAL 
    getCaps = lambda *_: GetKeyState(VK_CAPITAL)
else:
    getCaps = lambda *_: True


class CyborgLeagueBot:

    def __init__(self):
        self.Vision = VisionApi.Instance()
        self.Actions = Actions.Instance()
        self.running = False
        self.screen_elements = {}
    
    def Queue(self):
        os.system("clear")
        self.analyse_display()
        self.Actions.attackAllBuildings(bot.screen_elements)

    def analyse_display(self):
            img = self.Vision.screenshot()
            duration, result = self.Vision.upload(img)
            self.screen_elements = result
            self.Vision.runhook(result)
        

async def start():
    bot.running = True
    while bot.running:
        if bot.Vision.isReady() and getCaps():
            if bot.Vision.cooldown:
                time.sleep(0.5)
                bot.Vision.cooldown = False
            bot.Queue()
        else:
            bot.Vision.cooldown = True
            time.sleep(0.01)

bot = CyborgLeagueBot()

