from http import server
import os
import multiprocessing
import time
import asyncio

from flask import Flask
import flask_cors

from .Console import Console
from .GameActions import GameActions as Actions
from .GameStats import GameStats as Stats
from .Settings import Settings
from .Slaw import Slaw, SlawHelper
from .VisionApi import VisionApi

if os.name == 'nt':
    from win32api import GetKeyState
    from win32con import VK_CAPITAL 
    getCaps = lambda *_: GetKeyState(VK_CAPITAL)
else:
    getCaps = lambda *_: True


class CyborgLeagueBot:

    def __init__(self):
        Settings.init()
        lpath = Settings.get("client_LoL_loc")
        url = Settings.get("server_api_loc")

        self.Slaw = Slaw.SLAW(lpath=lpath)
        self.SlawHelper = SlawHelper.Instance(self.Slaw)
        self.Vision = VisionApi.Instance(url=url)
        self.Actions = Actions.Instance()
        self.Stats = Stats.Instance(Slaw=self.Slaw)
        self.running = False
        self.screen_elements = {}

        self.api_init()

        #p = self.Slaw.get("/lol-summoner/v1/current-summoner")
        #Console.log(f"Connected as: {Console.Fore.RED}{p['displayName']}{Console.Style.RESET_ALL} - {Console.Fore.CYAN}LVL{p['summonerLevel']}")

    def api_init(self):
        self.server = Flask(__name__)
        flask_cors.CORS(self.server)
        self.server.add_url_rule('/status','getstatus',view_func=lambda:"200")
        self.server.add_url_rule('/api/v1/getSummonerName','getSummonerName',view_func=self.SlawHelper.getSummonerName)
        self.server.add_url_rule('/api/v1/getSummonerLevel','getSummonerLevel',view_func=self.SlawHelper.getSummonerLevel)
        asyncio.run(self.api_run())

    async def api_run(self):
        self.server.run(port=34850,host="0.0.0.0")

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
        

def start():
    global bot
    bot = CyborgLeagueBot()
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

bot = None