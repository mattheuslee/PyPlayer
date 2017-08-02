import numpy as np

from game.basicgo import BasicGo
from game.player import Player

class MainApp:
    def __init__(self):
        self.basicGo = BasicGo()

    def playBasicGo(self):
        player = 1
        np.set_printoptions(linewidth = 100, formatter = { "int_kind": lambda x: "%3d" % x})
        while not self.basicGo.gameOver():
            print(self.basicGo.board.tiles)
            i, j = map(int, input().split())
            self.basicGo.set(i, j, player)
            player = Player.otherPlayer(player)
        print("Winner is " + str(self.basicGo.winner()))

if __name__ == "__main__":
    mainApp = MainApp()
    mainApp.playBasicGo()
