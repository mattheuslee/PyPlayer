import numpy as np

class MoveGame:
    def __init__(self, numCells):
        self.numCells = numCells
        self.stateSize = numCells
        self.actionSize = 2
        self.cells = np.zeros((numCells), dtype = "int32")
        self.playerPos = int(numCells / 2)
        self.hellPos = numCells - 1
        self.targetPos = 0
        self.cells[self.playerPos] = 1
        self.score = 0

    def step(self, action):
        reward = 0
        isDone = False
        self.cells[self.playerPos] = 0
        if action == 0: # move left
            self.playerPos -= 1
        else: # move right
            self.playerPos += 1
        if self.playerPos == self.targetPos: # reached target, game over
            reward = 1
            self.score = 1
            isDone = True
        elif self.playerPos == self.hellPos: # went to hell instead, game over
            reward = -1
            self.score = -1
            isDone = True
        self.cells[self.playerPos] = 1
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
        self.playerPos = int(self.numCells / 2)
        self.score = 0


