import os
from colorama import init, Fore, Back, Style
init()

def log(msg):
    print(f"{Style.DIM}{Fore.GREEN}[*] {Style.RESET_ALL}{Style.BRIGHT}{msg}")
