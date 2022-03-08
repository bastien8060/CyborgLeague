import json
import os
import requests
from flask import request

json_default = '''{
    "client_LoL_loc":"C:/Riot Games/League of Legends",
    "server_api_loc":"http://127.0.0.1:39743",
    "selected_champ":"None"
}'''

def init():
    if not os.path.exists("settings.json"):
        with open("settings.json","w") as file:
            file.write(json_default)
            file.close()

def get(key:str) -> str:
    with open("settings.json") as file:
        settings = json.loads(file.read())
    return settings[key]

def set(key:str) -> str:
    value = request.args.get('value')
    file = open("settings.json","r")
    settings = json.loads(file.read())
    file.close()
    settings[key] = value
    file = open("settings.json","w")
    file.write(json.dumps(settings))
    file.close()
    return "true"

def check():
    client_LoL_loc = get("client_LoL_loc")
    server_api_loc = get("server_api_loc")

    try:
        check1 = requests.get(server_api_loc).status_code == 200
    except:
        check1 = False
    check2 = os.path.isfile(os.path.join(client_LoL_loc, "LeagueClient.exe"))
    check3 = os.path.isfile(os.path.join(client_LoL_loc, "lockfile"))

    check = {"server":check1,"client_loc":check2,"client_running":check3}
    return json.dumps(check)