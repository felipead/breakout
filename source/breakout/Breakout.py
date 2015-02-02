from breakout.GameController import GameController

class Breakout:

    def __init__(self):
        self.controller = GameController()

    def run(self):
        self.controller.run()

if __name__ == "__main__":
    breakout = Breakout()
    breakout.run()