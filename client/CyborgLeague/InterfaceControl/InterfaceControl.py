from .Keyboard import KeyboardInstance
from .Mouse import MouseInstance

class Instance:
    def __init__(self, url="http://127.0.0.1:44444"):
        self.Mouse = MouseInstance()
        self.Keyboard = KeyboardInstance()