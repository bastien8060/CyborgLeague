class Instance():
    def __init__(self, Slaw):
        self.slaw = Slaw
    
    def getSummonerName(self):
        return self.slaw.get("/lol-summoner/v1/current-summoner")['displayName']

    def getSummonerLevel(self):
        return str(self.slaw.get("/lol-summoner/v1/current-summoner")['summonerLevel'])