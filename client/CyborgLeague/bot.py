import asyncio
import json
import math
import multiprocessing
import os
import time
from ast import arg
from http import server
from threading import Thread

import flask_cors
from flask import Flask

from .Console import Console
from .GameActions import GameActions as Actions
from .GameStats import GameStats as Stats
from .Settings import Settings
from .Slaw import Slaw, SlawHelper
from .VisionApi import VisionApi, VisionHelper

if os.name == 'nt':
    from win32api import GetKeyState
    from win32con import VK_CAPITAL 
    getCaps = lambda *_: GetKeyState(VK_CAPITAL)
else:
    getCaps = lambda *_: True


class CyborgLeagueBot:

    def __init__(self):
        
        Settings.init()
        self.Slaw = Slaw.SLAW()
        self.SlawHelper = SlawHelper.Instance()
        self.Vision = VisionApi.Instance()
        self.VHelper = VisionHelper.Instance()
        self.Stats = Stats.Instance()
        self.Actions = Actions.Instance()
        self.running = False
        self.screen_elements = {}

        self.api_init()

    def init(self):
        Settings.init()
        lpath = Settings.get("client_LoL_loc")
        url = Settings.get("server_api_loc")

        self.Slaw.init(lpath=lpath)
        self.Vision.init(url=url)
        self.SlawHelper.init(self.Slaw)
        self.Stats.init(Slaw=self.Slaw)

        p = self.Slaw.get("/lol-summoner/v1/current-summoner")
        Console.log(f"Connected as: {Console.Fore.RED}{p['displayName']}{Console.Style.RESET_ALL} - {Console.Fore.CYAN}LVL{p['summonerLevel']}")


    def start(self):
        self.init()
        self.running = True
        return "200"

    def stop(self):
        self.running = False
        return "200"

    def api_init(self):
        self.server = Flask(__name__)
        flask_cors.CORS(self.server)
        self.server.register_error_handler(500, lambda *_:("error has occured",500))
        self.server.add_url_rule('/status','getstatus',view_func=lambda:"true" if self.running else "false")
        self.server.add_url_rule('/api/v1/getSummonerName','getSummonerName',view_func=self.SlawHelper.getSummonerName)
        self.server.add_url_rule('/api/v1/getSummonerLevel','getSummonerLevel',view_func=self.SlawHelper.getSummonerLevel)
        self.server.add_url_rule('/api/v1/stop','stop_bot',view_func=self.stop)
        self.server.add_url_rule('/api/v1/start','start_bot',view_func=self.start)
        self.server.add_url_rule('/api/v1/getSetting/<key>','getSetting',view_func=Settings.get)
        self.server.add_url_rule('/api/v1/setSetting/<key>','setSetting',view_func=Settings.set)
        self.server.add_url_rule('/api/v1/checkSettings','setSettings',view_func=Settings.check)
        thread = Thread(target=self.api_run)
        thread.daemon = True
        thread.start()

    def api_run(self):
        asyncio.run(self.server.run(port=34850,host="0.0.0.0"))

    def Queue(self):
        os.system("cls")
        self.analyse_display()
        print("Abilities Level:",self.Stats.getAbilitiesLvl())
        print("Money:",self.Stats.getGold())
        print(self.getAction())

    def analyse_display(self):
        self.Stats.reload()
        championCodename = "Xayah".replace(" ","").replace("'","").replace(".","")
        img = self.Vision.screenshot()
        duration, result = self.Vision.upload(img,champions=[championCodename])
        result["minimap"] = json.loads(result["minimap"])
        self.screen_elements = result
        self.Vision.runhook(result)
        self.VHelper.refresh(result)
        self.Actions.Movement.update(result, self.Stats.getEvents())

    def getMinimapLocationByChampion(self,name):
        minimap = self.screen_elements["minimap"]
        for champion in minimap:
            if champion["champion"] != name:
                continue
            return self.Actions.Movement.createMinimapZone(champion["location"][0],champion["location"][1])
        return self.Actions.Movement.createMinimapZone(94,237)


    def getAction(self):
        gold = math.floor(self.Stats.getGold())
        championName = self.Stats.getChampionName()
        championLevel = self.Stats.getLevel()
        championCodename = "Xayah".replace(" ","").replace("'","").replace(".","")
        championLocation = self.getMinimapLocationByChampion(championCodename)

        scr_elements = self.screen_elements
        
        self.Actions.Shop.updateWallet(gold)

        if self.Stats.getGameTime() < 6:
            return
        
        if self.Stats.getHP() < 1:
            self.Stats.died()
            time.sleep(1)

        if (
            self.Stats.getLevel() == 1
            and self.Stats.getGameTime() > 5
            and self.Stats.getGameTime() < 50
            and not self.Stats.didBuyStarterPack()
        ):
            time.sleep(5)
            self.Actions.Shop.toggle()
            self.Actions.Shop.build_item("1055")
            self.Actions.Shop.build_item("2003")
            self.Stats.boughtStarterPack()
            self.Actions.Shop.toggle()
            time.sleep(2)
            self.Actions.Player.levelUpAbility(championLevel,championName)
            time.sleep(5)
        if (self.Stats.revived()):
            self.Actions.Shop.buildNextRecommended()
        if (self.Stats.hasLeveledUp()):
            self.Actions.Player.levelUpAbility(championLevel,championName)
        if (self.Stats.isHalfLife()):
            self.Actions.Player.useItemSlot(2)
        if (self.Stats.isLowLife()):
            self.Actions.Player.useSummonerSpell(1)
            self.Actions.Player.useSummonerSpell(2)
            self.Actions.Player.useItemSlot(2)
        if (self.Stats.isLowLife() or self.Stats.isRich()):
            self.Actions.Movement.fallback(championLocation)
            time.sleep(7)
            self.Actions.Player.useSummonerSpell(3)
            time.sleep(15)
            self.Actions.Shop.buildNextRecommended()
            time.sleep(3)
            lane = self.Actions.Movement.createMinimapZone(118, 236)
            self.Actions.Movement.clickOnMinimap(lane)
            time.sleep(3)
            pass
        if (self.Stats.isTakingDamage()):
            self.Actions.Movement.fallback(championLocation)
        if (not self.VHelper.allyMinionsVisible()
            and not self.VHelper.enemyVisible()
        ):
            lane = self.Actions.Movement.createMinimapZone(118, 236)
            self.Actions.Movement.clickOnMinimap(lane)
        if (self.VHelper.allyMinionsVisible()
            and not self.VHelper.enemyVisible()
        ):
            self.Actions.followAllMinions(scr_elements)
        if (self.VHelper.allyVisible() < 1
            and self.VHelper.enemyVisible()
        ):
            self.Actions.Movement.fallback(championLocation)
        if (self.VHelper.enemyVisible() and self.VHelper.allyVisible()):
            building_fight_condition = (
                self.VHelper.allyMinionsVisible(attackTurret=True) > self.VHelper.enemyMinionsVisible()
                and self.VHelper.allyMinionsVisible(attackTurret=True) > 3
                and self.VHelper.enemyChampionsVisible() == 0
                and self.VHelper.enemyBuildingsVisible() > 0
            )

            minion_fight_condition = (
                (
                    self.VHelper.allyMinionsVisible() > (self.VHelper.enemyMinionsVisible()/2)
                    or (self.VHelper.allyMinionsVisible() and self.VHelper.allyBuildingsVisible())
                    or (self.VHelper.allyMinionsVisible() > 2 and self.VHelper.allyChampionsVisible())
                ) 
                #and not self.VHelper.enemyChampionsVisible() #testremove
                and not self.VHelper.enemyBuildingsVisible()
            )

            champion_fight_condition = (
                self.VHelper.enemyChampionsVisible() > 0
                and (
                    (self.VHelper.allyMinionsVisible() and self.VHelper.allyBuildingsVisible())
                    or (self.VHelper.allyMinionsVisible() > self.VHelper.enemyMinionsVisible())
                )
                and (
                    self.VHelper.enemyChampionsVisible() < 3
                    or self.VHelper.allyChampionsVisible() > self.VHelper.enemyChampionsVisible()
                )
                and not self.VHelper.enemyBuildingsVisible()
            )

            if building_fight_condition:
                self.Actions.attackAllBuildings(scr_elements)

            elif champion_fight_condition:
                self.Actions.attackAllChampions(scr_elements)

            elif minion_fight_condition:
                self.Actions.attackNearbyMinion(scr_elements)
        
            else:
                if self.VHelper.allyBuildingsVisible():
                    return
                self.Actions.Movement.fallback(championLocation)

        

def start():
    global bot
    bot = CyborgLeagueBot()
    while True:
        if bot.Vision.isReady() and getCaps() and bot.running:
            if bot.Vision.cooldown:
                time.sleep(0.5)
                bot.Vision.cooldown = False
            bot.Queue()
        else:
            bot.Vision.cooldown = True
            time.sleep(0.01)

bot = None
