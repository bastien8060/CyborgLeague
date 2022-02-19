import json
import os


json_default = '''{
    "client_LoL_loc":"D:\\\\Riot Games\\\\League of Legends",
    "server_api_loc":"http://127.0.0.1:44444"
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