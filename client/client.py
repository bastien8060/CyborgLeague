import asyncio
import multiprocessing
import sys
from distutils.log import debug
import os

import webview
from flask import Flask, render_template, send_from_directory

from CyborgLeague import bot


class CyborgLeagueLoopInstance:
    def __init__(self):
        pass

    def start(self):
        asyncio.run(bot.start())

    def shutdown_handler(self):
        print('Shutting Down... ')
        self.process.terminate()
        sys.exit(0)

    def shutdown_handler_init(self,process):
        self.process = process

class GUI():
    def shutdown(self):
        return self.window.destroy()

    def minimize(self):
        self.window.minimize()
        return "200"
        

    def __init__(self,ThreadHandler):
        self.ThreadHandler = ThreadHandler

        self.server = Flask(__name__, static_folder='./CyborgLeague/Web', template_folder='./CyborgLeague/Web')
        self.server.add_url_rule('/', 'home', view_func=lambda:render_template("index.html"))
        self.server.add_url_rule('/<path:path>','server',view_func=lambda path:send_from_directory('CyborgLeague/Web', path))
        self.server.add_url_rule('/api/v1/shutdown','shutdown_api',view_func=self.shutdown)
        self.server.add_url_rule('/api/v1/minimize','minimize_api',view_func=self.minimize)

        self.window = webview.create_window('CyborgLeague',self.server,width=1450, height=740,resizable=False,frameless=True,easy_drag=True)
        self.window.expose(self.minimize, self.shutdown)
        
        self.splashscreen_handler()

        webview.start(http_server=True,debug=True,gui="cef")
        self.ThreadHandler.shutdown_handler()

    def splashscreen_handler(self):
        try:
            import pyi_splash
            pyi_splash.update_text('Loaded!')
            pyi_splash.close()
        except:
            pass


def main():
    CyborgLeagueLoop = CyborgLeagueLoopInstance()
    CyborgLeagueThread = multiprocessing.Process(target=CyborgLeagueLoop.start)
    CyborgLeagueLoop.shutdown_handler_init(CyborgLeagueThread)
    CyborgLeagueThread.start()

    GUI(CyborgLeagueLoop)



if __name__ == "__main__":
    main()


