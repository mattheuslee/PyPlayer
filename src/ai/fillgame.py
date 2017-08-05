import numpy as np

class FillGame:
    def __init__(self, numCells):
        self.numCells = numCells
        self.stateSize = numCells
        self.actionSize = numCells
        self.cells = np.zeros((numCells), dtype = "int32")

    def step(self, action):
        reward = 0
        if self.cells[action] == 0:
            self.cells[action] = 1
            reward = 1
        isDone = True
        for cell in self.cells:
            if cell == 0:
                isDone = False
        return (self.cells, reward, isDone)

    def state(self):
        return self.cells

    def output(self):
        for cell in self.cells:
            print(str(cell), end = " ")
        print("")

    def reset(self):
        self.cells = np.zeros((self.numCells), dtype = "int32")
