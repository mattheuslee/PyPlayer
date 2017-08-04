import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from ai.fillgame import FillGame

class DeepQLearningAgent:
    def __init__(self, stateSize, actionSize):
        self.stateSize = stateSize
        self.actionSize = actionSize
        self.memory = deque(maxlen = 2000)
        self.gamma = 0.95 # future reward discount rate
        self.epsilon = 1.0 # exploration rate, or how often we try random actions
        self.epsilonMin = 0.01
        self.epsilonDecay = 0.999
        self.learningRate = 0.001
        self.model = self.buildModel()

    def buildModel(self):
        model = Sequential()
        model.add(Dense(24, input_dim = self.stateSize, activation = "relu"))
        model.add(Dense(24, activation = "relu"))
        model.add(Dense(self.actionSize, activation = "relu"))
        model.compile(loss = "mse", optimizer = Adam(lr = self.learningRate))

    def addToMemory(self, state, action, reward, nextState, isDone):
        self.memory.append((state, action, reward, nextState, isDone))

    def act(self, state):
        if np.random.rand() <= self.epsilon: # time to try a random action
            return random.randrange(self.actionSize)
        actValues = self.model.predict(state) # get the predicted Q-values
        return np.argmax(actValues[0]) # choose the action with the highest Q-value

    def replay(self, batchSize):
        batch = random.sample(self.memory, batchSize)
        for state, action, reward, nextState, isDone in batch:
            target = reward # we're trying to predict actual reward amount
            if not isDone: # predict using actual award as well as predicted discounted future reward
                target = reward + self.gamma * np.amax(self.model.predict(nextState)[0])
            targetQValues = self.model.predict(state)
            targetQValues[0][action] == target # replace field in predicted reward with actual reward for action
            self.model.fit(state, targetQValues, epochs = 1, verbose = 0)
        if self.epsilon > self.epsilonMin:
            self.epsilon *= self.epsilonDecay
