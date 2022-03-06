import time
from pynput.mouse import Button, Controller


class MouseInstance():
    def resetMouse(self):
        self.mouse.position = (0, 0)
        
    def click(self, x:int, y:int) -> True:
        self.mouse.position = (x,y)
        self.mouse.press(Button.left)
        time.sleep(0.1)
        self.mouse.release(Button.left)

    def rightClick(self, x:int, y:int) -> True:
        self.mouse.position = (x,y)
        self.mouse.press(Button.right)
        time.sleep(0.1)
        self.mouse.release(Button.right)



    def __init__(self):
        self.mouse = Controller()
