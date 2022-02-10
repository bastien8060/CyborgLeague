# pylint: skip-file
import os
from colorama import init, Fore, Back, Style
from slaw import SLAW
init()

def log(msg):
    print(f"{Style.DIM}{Fore.GREEN}[*] {Style.RESET_ALL}{msg}")

def clear():
    print(chr(27) + "[2J",end="")

clear()
slaw = SLAW()
print(slaw.authorization)
p = slaw.get("/lol-summoner/v1/current-summoner")
log(f"{Style.BRIGHT}Connected as: {Fore.RED}{p['displayName']}{Style.RESET_ALL} - {Fore.CYAN}LVL{p['summonerLevel']}")


try:
    all = slaw.get_live("/liveclientdata/allgamedata")
    print(all)
    with open("allgamedata","w") as f:
        f.write(str(all))
        f.close()
except Exception as e:
    print(e)

#LeagueClient:3028:51231:Lkan3Oote5dHHFOcjZUf4Q:https
#https://127.0.0.1:51231/lol-summoner/v1/current-summoner
