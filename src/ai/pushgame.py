import random
import numpy as np

class PushGame:
    PLAYER_VAL = 55
    BOX_VAL = 155
    TARGET_VAL = 255
    def __init__(self, numCells):
        self.numCells = numCells
        self.stateSize = numCells
        self.actionSize = 2
        self.cells = np.zeros((numCells), dtype = "int32")
        self.playerPos = 0
        self.targetPos = numCells - 1
        self.boxPos = int(numCells / 3)
        self.cells[self.playerPos] = self.PLAYER_VAL
        self.cells[self.targetPos] = self.TARGET_VAL
        self.cells[self.boxPos] = self.BOX_VAL

    def step(self, action):
        reward = 0
        isDone = False
        self.cells[self.playerPos] = 0
        self.cells[self.boxPos] = 0
        if action == 0: # move left
            if self.playerPos > 0:
                self.playerPos -= 1
        else: # move right
            if self.playerPos == self.boxPos - 1: # pushes the box
                self.playerPos += 1
                self.boxPos += 1
                if self.boxPos == self.targetPos: # box reached target, game over
                    reward = 1
                    isDone = True
            else:
                self.playerPos += 1
        self.cells[self.playerPos] = self.PLAYER_VAL
        self.cells[self.boxPos] = self.BOX_VAL
        return (self.cells, reward, isDone)

    def state(self):
        return self.cells

    def output(self):
        stringOutput = ""
        for cell in self.cells:
            stringOutput = stringOutput + str(cell) + " "
        print("\r{}".format(stringOutput), end = "")

    def reset(self):
        self.cells[self.playerPos] = 0
        self.cells[self.boxPos] = 0
        self.playerPos = 0
        self.boxPos = int(self.numCells / 3)
        self.cells[self.playerPos] = self.PLAYER_VAL
        self.cells[self.boxPos] = self.BOX_VAL
        self.cells[self.targetPos] = self.TARGET_VAL




