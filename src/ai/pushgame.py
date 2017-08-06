import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Convolution2D, Flatten
from keras.optimizers import Adam

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
        self.boxPos = int(self.NUM_CELLS / 3)
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
        self.cells = np.zeros((self.I_DIM, self.J_DIM), dtype = "int32")
        self.playerPos = np.array([0, 0], dtype = "int32")
        self.boxPos = np.array([int(self.I_DIM / 3), int(self.J_DIM / 3)], dtype = "int32")
        self.targetPos = np.array([int(self.I_DIM - 1), int(self.J_DIM - 1)], dtype = "int32")
        self.hellPos = np.array([(0, 0), (self.I_DIM - 1, 0), (0, self.J_DIM - 1)], dtype = "int32")

        self.cells[self.playerPos[0]][self.playerPos[1]] = self.PLAYER_VAL
        self.cells[self.boxPos[0]][self.boxPos[1]] = self.BOX_VAL
        self.cells[self.targetPos[0]][self.targetPos[1]] = self.TARGET_VAL

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
        self.cells[self.playerPos[0]][self.playerPos[1]] = 0
        self.cells[self.boxPos[0]][self.boxPos[1]] = 0
        if action == 0: # move left
            if (self.playerPos[0] == self.boxPos[0]
                    and self.playerPos[1] - 1 == self.boxPos[1]
                    and self.boxPos[1] > 0): # pushes the box
                self.playerPos[1] -= 1
                self.boxPos[1] -= 1
            elif self.playerPos[1] > 0: # just move
                self.playerPos[1] -= 1
        elif action == 1: # move right
            if (self.playerPos[0] == self.boxPos[0]
                    and self.playerPos[1] == self.boxPos[1] - 1
                    and self.boxPos[1] != self.J_DIM - 1): # pushes the box
                self.playerPos[1] += 1
                self.boxPos[1] += 1
            elif self.playerPos[1] != self.J_DIM - 1: # just move
                self.playerPos[1] += 1
        elif action == 2: # move up
            if (self.playerPos[0] - 1 == self.boxPos[0]
                    and self.playerPos[1] == self.boxPos[1]
                    and self.boxPos[0] > 0): # pushes the box
                self.playerPos[0] -= 1
                self.boxPos[0] -= 1
            elif self.playerPos[0] > 0: # just move
                self.playerPos[0] -= 1
        else: # move down
            if (self.playerPos[0] == self.boxPos[0] - 1
                    and self.playerPos[1] == self.boxPos[1]
                    and self.boxPos[0] != self.I_DIM - 1): # pushes the box
                self.playerPos[0] = 1
                self.boxPos[0] += 1
            elif self.playerPos[0] != self.I_DIM - 1: # just move
                self.playerPos[0] += 1

        if np.array_equal(self.boxPos, self.targetPos): # box reached the target
            reward = 1
            isDone = True
        elif (np.array_equal(self.boxPos, self.hellPos[0])   # pushed box into unreachable area,
             or np.array_equal(self.boxPos, self.hellPos[1]) # game over
             or np.array_equal(self.boxPos, self.hellPos[2])):
            reward = -1
            isDone = True
        else:
            self.cells[self.playerPos[0]][self.playerPos[1]] = self.PLAYER_VAL
            self.cells[self.boxPos[0]][self.boxPos[1]] = self.BOX_VAL

        return (self.state(), reward, isDone)

    def state(self):
        return np.reshape(self.cells, (1, self.I_DIM, self.J_DIM))

    def output(self):
        stringOutput = ""
        for row in self.cells:
            for cell in row:
                tempOutput = "%4s" % str(cell)
                stringOutput = stringOutput + tempOutput
            stringOutput = stringOutput + "\n"
        print("\r{}".format(stringOutput))

    def reset(self):
        self.cells[self.playerPos[0]][self.playerPos[1]] = 0
        self.cells[self.boxPos[0]][self.boxPos[1]] = 0
        self.playerPos = np.array([0, 0], dtype = "int32")
        self.boxPos = np.array([int(self.I_DIM / 3), int(self.J_DIM / 3)], dtype = "int32")
        self.cells[self.playerPos[0]][self.playerPos[1]] = self.PLAYER_VAL
        self.cells[self.boxPos[0]][self.boxPos[1]] = self.BOX_VAL
        self.cells[self.targetPos[0]][self.targetPos[1]] = self.TARGET_VAL



