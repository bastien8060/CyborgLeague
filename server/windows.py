import atexit
import os
import shutil
import subprocess
import sys
import threading
import time

import pyuac
import win32api
import win32con
import win32event
import win32ui
from infi.systray import SysTrayIcon
from pywin.mfc import dialog
from tendo import singleton
from win32com.shell import shell, shellcon


def MakeDlgTemplate(name):
    style = (
        win32con.DS_MODALFRAME
        | win32con.WS_POPUP
        | win32con.WS_VISIBLE
        | win32con.WS_CAPTION
        | win32con.WS_SYSMENU
        | win32con.DS_SETFONT
    )
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE

    w = 215
    h = 36

    dlg = [
        [
            name,
            (0, 0, w, h),
            style,
            None,
            (8, "MS Sans Serif"),
        ],
    ]

    s = win32con.WS_TABSTOP | cs

    return dlg


class MakeDialog(dialog.Dialog):
    def OnInitDialog(self):
        self.slow = False
        rc = dialog.Dialog.OnInitDialog(self)
        self.pbar = win32ui.CreateProgressCtrl()
        self.running = True
        self.pbar.CreateWindow(
            win32con.WS_CHILD | win32con.WS_VISIBLE, (10, 10, 310, 24), self, 1001
        )
        # self.pbar.SetStep (5)
        self.progress = 0
        self.pincr = 1
        threading.Timer(0,self.autoincrement,()).start()
        return rc
    
    def finish(self):
        self.running = False
        self.pbar.SetPos(100)
        time.sleep(2)
        self.OnCancel()

    def autoincrement_slow(self):
        for _ in range(65):
            time.sleep(0.10)
            self.OnOK()
        time.sleep(1)
        for _ in range(24):
            time.sleep(0.4)
            self.OnOK()
        for _ in range(10):
            self.OnOK()
            time.sleep(0.8)

    def autoincrement(self):
        if self.slow:
            return self.autoincrement_slow()
        for _ in range(65):
            time.sleep(0.05)
            self.OnOK()
        time.sleep(1)
        for _ in range(24):
            time.sleep(0.2)
            self.OnOK()
        for _ in range(10):
            self.OnOK()
            time.sleep(0.5)

    def OnOK(self):
        # NB: StepIt wraps at the end if you increment past the upper limit!
        # self.pbar.StepIt()
        if not self.running:
            return
        self.progress = self.progress + self.pincr
        if self.progress > 100:
            self.progress = 100
        if self.progress <= 100:
            self.pbar.SetPos(self.progress)

try:
    instance = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
except:
    print("Close CyborgLeague Server first before launching it again.")
    os._exit(0)


def confirm(msg,title,cancel=True):
    opt = win32con.MB_YESNOCANCEL if cancel else win32con.MB_YESNO

    response = win32ui.MessageBox(msg, title, opt)
    if response == win32con.IDYES:
        return True
    elif response == win32con.IDNO:
        return False
    elif response == win32con.IDCANCEL:
        return False

def installWSL():
    commands = "powershell Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart"
    #nShow=win32con.SW_SHOWNORMAL
    event = shell.ShellExecuteEx(fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,lpVerb='runas', lpFile='powershell.exe', lpParameters=commands)
    hprocess = event['hProcess']
    d = MakeDialog(MakeDlgTemplate("Installing WSL2"))
    d.slow = False
    thread = threading.Thread(target=d.DoModal,args=())
    thread.start()
    win32event.WaitForSingleObject(hprocess, win32event.INFINITE) 
    d.finish()

def checkWSLDistro():
    testing_process = subprocess.run(["wsl", "test", "-f", "/etc/os-release"])
    if testing_process.returncode == 0:
        return True
    return False

def checkSetupDistro():
    testing_process = subprocess.run(["wsl.exe", "-u", "root", "test", "-f", "/root/.CyborgLeagueInstalled"])
    if testing_process.returncode == 0:
        return True
    return False

if (not shutil.which("wsl")):
    if (confirm("Microsoft WSL2 (Windows Subsystem for Linux v2) is not installed. \n\nDo you want to install it?","CyborgLeague")):
        t = installWSL()
        if (confirm("To finish, we need to restart this PC, do you want to go ahead now? This will take under 5 minutes!","CyborgLeague",cancel=False)):
            win32api.InitiateSystemShutdown(None, "Finalizing WSL2 Installation!", 0, 1, 1)
    exit()

if not checkWSLDistro():
    if (confirm("Almost done! The last step is installing a WSL2 Distro.\n\nDo you wish to proceed (Microsoft Store)?","CyborgLeague")):
        subprocess.Popen('powershell.exe start ms-windows-store://pdp/?ProductId=9NBLGGH4MSV6')
        time.sleep(1)
    exit()

if not checkSetupDistro():
    cmd = "cd /root;sudo add-apt-repository ppa:deadsnakes/ppa -y;apt update -y;apt install git python3.6 -y;wget https://bootstrap.pypa.io/pip/3.6/get-pip.py;python3.6 get-pip.py;python3.6 get-pip.py;pip install opencv-python requests numpy flask bjoern;git clone https://github.com/bastien8060/CyborgLeague;rm get-pip.py;touch ~/.CyborgLeagueInstalled"
    installProcess = subprocess.Popen(f'wsl.exe -u root bash -c "{cmd}" ')

    d = MakeDialog(MakeDlgTemplate("Setting up CyborgLeague in WSL2"))
    d.slow = True
    thread = threading.Thread(target=d.DoModal,args=())
    thread.start()
    installProcess.communicate()
    d.finish()
else:
    updateProcess = subprocess.Popen(f'wsl.exe -u root bash -c "cd /root/CyborgLeague;git pull" ')
    d = MakeDialog(MakeDlgTemplate("Updating CyborgLeague Server"))
    d.slow = False
    thread = threading.Thread(target=d.DoModal,args=())
    thread.start()
    updateProcess.communicate()
    d.finish()

def cleanup():
    server_process.kill()
    os._exit(0)

server_process = subprocess.Popen('wsl.exe -u root bash -c "cd ~/CyborgLeague/server;python3.6 unix.py"')

with SysTrayIcon("../src/logo.ico", "CyborgLeague Server Starting...",on_quit=lambda _:cleanup()) as systray:
    systray.update(hover_text="CyborgLeague Server Running")

server_process.communicate()
