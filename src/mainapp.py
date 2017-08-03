import sys
import time
import numpy as np

from ai.basicgoai import BasicGoAi
from game.basicgo import BasicGo
from game.player import Player

class MainApp:
    def human_human_basicgo():
        basicGo = BasicGo()
        player = -1
        np.set_printoptions(linewidth = 100, formatter = { "int_kind": lambda x: "%3d" % x})
        while not basicGo.gameOver():
            print(basicGo.board.tiles)
            print("Current turn: " + str(basicGo.turn) + " Current score: " + str(basicGo.score))
            i, j = map(int, input().split())
            basicGo.set(i, j, player)
            player = Player.otherPlayer(player)
        print("Winner is " + str(basicGo.winner()))

    def human_ai_basicgo():
        basicGo = BasicGo()
        player = -1
        basicGoAi = BasicGoAi(1)
        np.set_printoptions(linewidth = 100, formatter = { "int_kind": lambda x: "%3d" % x})
        while not basicGo.gameOver():
            print(basicGo.board.tiles)
            print("Current turn: " + str(basicGo.turn) + " Current score: " + str(basicGo.score))
            i, j = map(int, input().split())
            basicGo.set(i, j, player)
            i, j = basicGoAi.getMove(basicGo)
            basicGo.set(i, j, Player.otherPlayer(player))
        print("Winner is " + str(basicGo.winner()))

    def ai_ai_basicgo():
        basicGo = BasicGo()
        player = -1
        basicGoAi = BasicGoAi(-1)
        basicGoAi2 = BasicGoAi(1)
        np.set_printoptions(linewidth = 100, formatter = { "int_kind": lambda x: "%3d" % x})
        while not basicGo.gameOver():
            i, j = basicGoAi.getMove(basicGo)
            basicGo.set(i, j, player)
            print(basicGo.board.tiles)
            print("Current turn: " + str(basicGo.turn) + " Current score: " + str(basicGo.score) + "\n\n")
            time.sleep(0.1)
            i, j = basicGoAi2.getMove(basicGo)
            basicGo.set(i, j, Player.otherPlayer(player))
            print(basicGo.board.tiles)
            print("Current turn: " + str(basicGo.turn) + " Current score: " + str(basicGo.score) + "\n\n")
            time.sleep(0.1)
        print("Winner is " + str(basicGo.winner()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error, type of game must be given")
    elif sys.argv[1] == "hhbg":
        MainApp.human_human_basicgo()
    elif sys.argv[1] == "habg":
        MainApp.human_ai_basicgo()
    elif sys.argv[1] == "aabg":
        MainApp.ai_ai_basicgo()
