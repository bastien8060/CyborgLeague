import client.CyborgLeague.VisionApi as VisionApi

class CyborgLeagueBot:
    def __init__(self):
        self.running = False

async def start():
    bot.running = True
    while bot.running:
        img = VisionApi.screenshot()
        VisionApi.upload(img)

bot = CyborgLeagueBot()

