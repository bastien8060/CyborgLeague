import asyncio
import signal
import sys

from CyborgLeague import bot


def shutdown_handler(signal, frame):
    print('Shutting Down... ')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, shutdown_handler)
    asyncio.run(bot.start())

if __name__ == "__main__":
    main()


