import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Convolution2D, Flatten
from keras.optimizers import Adam

I = 0
J = 1

class PushGame1D:
    NUM_CELLS = 10

    PLAYER_VAL = 55
    BOX_VAL = 155
    TARGET_VAL = 255

    def __init__(self):
        self.stateSize = self.NUM_CELLS
        self.actionSize = 2
        self.cells = np.zeros((self.NUM_CELLS), dtype = "int32")
        self.playerPos = 0
        self.targetPos = self.NUM_CELLS - 1
        self.boxPos = int(self.NUM_CELLS / 3)
        self.cells[self.playerPos] = self.PLAYER_VAL
        self.cells[self.targetPos] = self.TARGET_VAL
        self.cells[self.boxPos] = self.BOX_VAL

    def buildModel(self, learningRate):
        model = Sequential()
        hiddenNodes = int(self.stateSize * 0.8)
        model.add(Dense(hiddenNodes, input_dim = self.stateSize, activation = "relu"))
        model.add(Dense(hiddenNodes, activation = "relu"))
        model.add(Dense(self.actionSize, activation = "linear")) # linear due to negative reward
        model.compile(loss = "mse", optimizer = Adam(lr = learningRate))
        return model

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

class PushGame2D:
    I_DIM = 4
    J_DIM = 4

    PLAYER_VAL = 55
    BOX_VAL = 155
    TARGET_VAL = 255

    def __init__(self):
        self.stateSize = self.I_DIM * self.J_DIM
        self.actionSize = 4
        self.cells = np.zeroes((self.I_DIM, self.J_DIM), dtype = "int32")
        self.playerPos = (0, 0)
        self.boxPos = (int(self.I_DIM / 3), int(self.J_DIM / 3))
        self.targetPos = (self.I_DIM - 1, self.J_DIM - 1)
        self.hellPos = ((0, 0), (self.I_DIM - 1, 0), (0, self.J_PIM - 1))

        self.cells[self.playerPos[I]][self.playerPos[J]] = self.PLAYER_VAL
        self.cells[self.boxPos[I]][self.boxPos[J]] = self.BOX_VAL
        self.cells[self.targetPos[I]][self.targetPos[J]] = self.TARGET_VAL

    def buildModel(self, learningRate):
        model = Sequential()
        numConvNodes = 5
        convSize = 2
        model.add(Convolution2D(numConvNodes, (convSize, convSize), activation = "relu", input_shape = (self.I_DIM, self.J_DIM, 1)))
        model.add(Flatten())
        hiddenNodes = self.I_DIM * self.J_DIM
        model.add(Dense(hiddenNodes, activation = "relu"))
        model.add(Dense(self.actionSize, activation = "linear")) # linear due to negative reward
        model.compile(loss = "mse", optimizer = Adam(lr = learningRate))
        return model

    def step(self, action):
        reward = 0
        isDone = False
        self.cells[self.playerPos[I]][self.playerPos[J]] = 0
        self.cells[self.boxPos[I]][self.boxPos[J]] = 0
        if action == 0: # move left
            if self.playerPos[J] - 1 == self.boxPos[J]: # pushes the box
                self.playerPos[J] -= 1
                self.boxPos[J] -= 1
            elif self.playerPos[J] > 0: # just move
                self.playerPos[J] -= 1
        elif action == 1: # move right
            if self.playerPos[J] = self.boxPos[J] - 1: # pushes the box
                self.playerPos[J] += 1
                self.boxPos[J] += 1
            elif self.playerPos[J] != self.J_DIM - 1: # just move
                self.playerPos[J] += 1
        elif action == 2: # move up
            if self.playerPos[I] - 1 = self.boxPos[I]: # pushes the box
                self.playerPos[I] -= 1
                self.boxPos[I] -= 1
            elif self.playerPos[I] > 0: # just move
                self.playerPos[I] -= 1
        else: # move down
            if self.playerPos[I] = self.boxPos[I] - 1: # pushes the box
                self.playerPos[I] += 1
                self.boxPos[I] += 1
            elif self.playerPos[I] != self.I_DIM - 1: # just move
                self.playerPos[I] += 1

        if cmp(self.boxPos, self.targetPos) == 0: # box reached the target
            reward = 1
            isDone = True
        elif cmp(self.boxPos, self.hellPos[0]) == 0 or
             cmp(self.boxPos, self.hellPos[1]) == 0 or
             cmp(self.boxPos, self.hellPos[2]) == 0: # pushed box into unreachable area, game over
            reward = -1
            isDone = True

        self.cells[self.playerPos[I]][self.playerPos[J]] = self.PLAYER_VAL
        self.cells[self.boxPos[I]][self.boxPos[J]] = self.BOX_VAL

        return (self.state(), reward, isDone)

    def state(self):
        return np.reshape(self.cells, (1, self.I_DIM, self.J_DIM))

    def output(self):
        stringOutput = ""
        for row in self.cells:
            for cell in row:
                stringOutput = stringOutput + str(cell) + " "
            stringOutput = stringOutput + "\n"
        print("\r{}".format(stringOutput), end = "")

    def reset(self):
        self.cells[self.playerPos[I]][self.playerPos[J]] = 0
        self.cells[self.boxPos[I]][self.boxPos[J]] = 0
        self.playerPos = (0, 0)
        self.boxPos = (int(self.I_DIM / 3), int(self.J_DIM / 3))
        self.cells[self.playerPos[I]][self.playerPos[J]] = self.PLAYER_VAL
        self.cells[self.boxPos[I]][self.boxPos[J]] = self.BOX_VAL
        self.cells[self.targetPos[I]][self.targetPos[J]] = self.TARGET_VAL
