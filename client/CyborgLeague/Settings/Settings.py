import json
import string

def get(key) -> string:
    with open("settings.json") as file:
        settings = json.loads(file.read())
    return settings[key]