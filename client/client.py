import asyncio
import signal
import sys
import os
import importlib

from CyborgLeague import bot

def splashscreen_handler():
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()

def shutdown_handler(signal, frame):
    print('Shutting Down... ')
    sys.exit(0)

def main():
    splashscreen_handler()
    signal.signal(signal.SIGINT, shutdown_handler)
    asyncio.run(bot.start())

if __name__ == "__main__":
    main()


