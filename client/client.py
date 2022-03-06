import asyncio
import multiprocessing
import os
import sys
from distutils.log import debug

import clr
import webview
from flask import Flask, render_template, send_from_directory

from CyborgLeague import bot


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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

        self.initialize_api_server()

        self.window = webview.create_window('CyborgLeague',
                                            self.server,
                                            width=1450, 
                                            height=740,
                                            resizable=False,
                                            frameless=True,
                                            easy_drag=True,
                                            background_color='#010A13')

        self.window.expose(self.minimize, self.shutdown)

        self.splashscreen_handler()

        webview.start(http_server=True,debug=True,gui="cef")
        self.ThreadHandler.shutdown_handler()

    def initialize_api_server(self):
        if getattr(sys, 'frozen', False):
            template_folder = resource_path('CyborgLeague/Web')
            static_folder = resource_path('CyborgLeague/Web')
            self.server = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        else:
            self.server = Flask(__name__, static_folder='./CyborgLeague/Web', template_folder='./CyborgLeague/Web')


        self.server.add_url_rule('/', 'home', view_func=lambda:render_template("index.html"))
        self.server.add_url_rule('/<path:path>','server',view_func=lambda path:send_from_directory('CyborgLeague/Web', path))
        self.server.add_url_rule('/api/v1/shutdown','shutdown_api',view_func=self.shutdown)
        self.server.add_url_rule('/api/v1/minimize','minimize_api',view_func=self.minimize)

    def splashscreen_handler(self):
        try:
            import pyi_splash
            pyi_splash.close()
        except:
            pass


def main():
    CyborgLeagueLoop = CyborgLeagueLoopInstance()
    multiprocessing.freeze_support()
    CyborgLeagueThread = multiprocessing.Process(target=CyborgLeagueLoop.start)
    CyborgLeagueThread.daemon=True
    CyborgLeagueLoop.shutdown_handler_init(CyborgLeagueThread)
    CyborgLeagueThread.start()

    GUI(CyborgLeagueLoop)



if __name__ == "__main__":
    main()
