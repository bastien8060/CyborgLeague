# CyborgLeague
A League of Legends bot to play and win a 5v5 game in Summoners Rift!

> This is an ongoing work which isnt completely finished yet! (WIP alert)

This bot will be able to play a game, and win in top/mid/bot using many factors in-game. 

This bot isn't made to carry a game however, although it possibly could in the near-future. This bot was made with the intention of making it play few minutes while the player is AFK, to avoid a temp-ban.

This bot does not take in consideration allies making it not ver suitable to play in the bot/mid lane (especially in the bot lane).

#### It can: 
- detect Enemy `wards`/`minions`/`champions`/`turret`
- check `wealth` (how much money the summoner has)
- check `HP`+`Mana/Energy` (total/max and remaining amount for your summoner)
- check the player's `LVL`+`Life Status` (if the player is alive or dead)

#### It will be able to:
- check all bought `Items` + can use the `Shop`
- detect Ally `wards`/`minions`/`champions`/`turret`

#### It perhaps will be able to:
- Make use of the minimap

## QuickStart

The service runs in two parts: 
- API Server (Image Recognition)
- Client Program (Plays League)

This will let you offload the intensive AI CPU work to another machine/PC in a later release of CyborgLeague.

It is recommended to run the API server on a Linux/WSL2 Machine which sees a 200% performance increase.

To install it:
```sh 
git clone https://github.com/bastien8060/CyborgLeague
```

To run the API server:
```sh
cd CyborgLeague/server
python unix.py #if you are running on wsl2/linux
python windows.py #if you are running on plain windows.
```

To run the client service:
```sh
cd CyborgLeague/client
python client.py
```

To enable the bot, you need to have the CAPLOCK on, on the same machine with the client running. You also need to be on the same window, that has League of Legend running.

