import os
import random

from game.player import Player

class BasicGoAi:
    def __init__(self, player):
        random.seed(os.urandom(0))
        self.player = player

    def getMove(self, basicGo):
        if basicGo.gameOver():
            return (0, 0)
        i = random.randrange(basicGo.iDim)
        j = random.randrange(basicGo.jDim)
        while Player.isPlayer(basicGo.get(i, j)):
            i = random.randrange(basicGo.iDim)
            j = random.randrange(basicGo.jDim)
        return (i, j)
