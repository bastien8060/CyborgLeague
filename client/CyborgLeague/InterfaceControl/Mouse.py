import time
from pynput.mouse import Button, Controller


class MouseInstance():
    def click(self, x:int, y:int) -> True:
        self.mouse.position = (x,y)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)

    def __init__(self):
        self.mouse = Controller()
