from graphicsT import Graphics
from graphicsT import PromptWindow
from engine import Engine


class runner():

    engine = Engine()

    def __init__(self):
       # prompt = PromptWindow()
        graphics = Graphics(self.engine)

