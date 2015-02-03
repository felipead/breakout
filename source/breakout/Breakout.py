from breakout.Controller import Controller


class Breakout:

    def __init__(self):
        self.controller = Controller()

    def run(self):
        self.controller.run()

if __name__ == "__main__":
    breakout = Breakout()
    breakout.run()