from breakout.game.GameController import GameController


class Breakout(object):

    def __init__(self):
        self.controller = GameController()

    def run(self):
        self.controller.run()

if __name__ == "__main__":
    breakout = Breakout()
    breakout.run()