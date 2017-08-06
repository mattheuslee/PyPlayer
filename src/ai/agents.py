import random
import time
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from ai.fillgame import FillGame
from ai.movegame import MoveGame
from ai.pushgame import PushGame

NUM_EPISODES = 10000

class DeepQLearningAgent:
    def __init__(self, stateSize, actionSize):
        self.stateSize = stateSize
        self.actionSize = actionSize
        self.memory = deque(maxlen = 100)
        self.gamma = 0.95 # future reward discount rate
        self.epsilon = 1.0 # exploration rate, or how often we try random actions
        self.epsilonMin = 0.01
        self.epsilonDecay = 0.999
        self.learningRate = 0.001
        self.model = self.buildModel()

    def buildModel(self):
        model = Sequential()
        model.add(Dense(8, input_dim = self.stateSize, activation = "relu"))
        model.add(Dense(8, activation = "relu"))
        model.add(Dense(self.actionSize, activation = "linear")) # using linear due to possibility of negative reward
        model.compile(loss = "mse", optimizer = Adam(lr = self.learningRate))
        return model

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

if __name__ == "__main__":
    NUM_CELLS = 10
    #game = FillGame(NUM_CELLS)
    #game = MoveGame(NUM_CELLS)
    game = PushGame(NUM_CELLS)
    stateSize = game.stateSize
    actionSize = game.actionSize
    agent = DeepQLearningAgent(stateSize, actionSize)
    isDone = False
    batchSize = 32

    for episode in range(NUM_EPISODES):
        game.reset()
        state = game.state()
        state = np.reshape(state, [1, stateSize])
        for t in range(500):
            action = agent.act(state)
            nextState, reward, isDone = game.step(action)
            nextState = np.reshape(nextState, [1, stateSize])
            agent.addToMemory(state, action, reward, nextState, isDone)
            state = nextState
            if isDone:
                print("\repisode: {}/{}, num moves: {}, e: {:.2}"
                      .format(episode, NUM_EPISODES, t + 1, agent.epsilon))
                if episode % 100 == 0:
                    time.sleep(1)
                break
            if episode % 100 == 0:
                game.output()
                time.sleep(0.1)
        if len(agent.memory) > batchSize:
            agent.replay(batchSize)






