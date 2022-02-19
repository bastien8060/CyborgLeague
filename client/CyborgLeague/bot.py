import os
import time

from .GameActions import GameActions as Actions
from .GameStats import GameStats as Stats
from .VisionApi import VisionApi
from .Slaw import Slaw
from .Console import Console
from .Settings import Settings

if os.name == 'nt':
    from win32api import GetKeyState
    from win32con import VK_CAPITAL 
    getCaps = lambda *_: GetKeyState(VK_CAPITAL)
else:
    getCaps = lambda *_: True


class CyborgLeagueBot:

    def __init__(self):
        lpath = Settings.get("client_LoL_loc")
        url = Settings.get("server_api_loc")

        self.Vision = VisionApi.Instance(url=url)
        self.Actions = Actions.Instance()
        self.Stats = Stats.Instance()
        self.Slaw = Slaw.SLAW(lpath=lpath)
        self.running = False
        self.screen_elements = {}

        p = self.Slaw.get("/lol-summoner/v1/current-summoner")
        Console.log(f"Connected as: {Console.Fore.RED}{p['displayName']}{Console.Style.RESET_ALL} - {Console.Fore.CYAN}LVL{p['summonerLevel']}")

    
    def Queue(self):
        os.system("cls")
        self.analyse_display()
        self.Stats.reload()
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

