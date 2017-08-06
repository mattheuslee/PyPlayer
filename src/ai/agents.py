import random
import time
import numpy as np
from collections import deque
from keras.models import load_model

from ai.pushgame import PushGame1D, PushGame2D

NUM_EPISODES = 10000

class DeepQLearningAgent:
    def __init__(self, game):
        self.stateSize = game.stateSize
        self.actionSize = game.actionSize
        self.memory = deque(maxlen = 1000)
        self.gamma = 0.9 # future reward discount rate
        self.epsilon = 1.0 # exploration rate, or how often we try random actions
        self.epsilonMin = 0.05
        self.epsilonDecay = 0.99
        self.learningRate = 0.001
        self.model = game.buildModel(self.learningRate)

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
    game = PushGame1D()
    #game = PushGame2D()
    agent = DeepQLearningAgent(game)
    stateSize = game.stateSize
    batchSize = 100

    interval = 100

    agent.model = load_model("push1D.h5")
    #agent.model.save("push1D.h5")

    for episode in range(NUM_EPISODES):
        game.reset()
        state = game.state()
        for t in range(500):
            action = agent.act(state)
            nextState, reward, isDone = game.step(action)
            nextState = np.reshape(nextState, [1, stateSize])
            agent.addToMemory(state, action, reward, nextState, isDone)
            state = nextState
            if isDone:
                print("\repisode: {}/{}, num moves: {}, reward: {}, e: {:.2}"
                      .format(episode, NUM_EPISODES, t + 1, reward, agent.epsilon))
                if episode % interval == 0:
                    time.sleep(1)
                break
            if episode % interval == 0:
                game.output()
                time.sleep(0.1)
        if len(agent.memory) > batchSize:
            agent.replay(batchSize)
        agent.model.save("push1D.h5")




