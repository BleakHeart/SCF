from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.pyplot as plt

sasso,carta,forbice = 0,1,2
NUM_ACTIONS = 3
oppStrategy = np.random.rand(NUM_ACTIONS)
oppStrategy = oppStrategy / np.sum(oppStrategy)

x = ["s", "c", "f"]
np.set_printoptions(precision=3, suppress=True)

def value(p1,p2):
    if p1==p2:
        return 0
    if (p1-1)%NUM_ACTIONS == p2:
        return 1
    else:
        return -1

def normalize(strategy):
    strategy = np.copy(strategy)
    normalizingSum = np.sum(strategy)
    if normalizingSum > 0:
        strategy /= normalizingSum
    else:
        strategy = np.ones(strategy.shape[0])/strategy.shape[0]
    return strategy

def getStrategy(regretSum):
    return normalize(np.maximum(regretSum, 0))

def getAverageStrategy(strategySum):
    return normalize(strategySum)

def getAction(strategy):
    strategy = strategy / np.sum(strategy)
    return np.searchsorted(np.cumsum(strategy), random.random())

def innerTrain(regretSum, strategySum, oppStrategy):
    strategy = getStrategy(regretSum)
    strategySum += strategy

    myAction = getAction(strategy)
    otherAction = getAction(oppStrategy)

    # per sasso carta forbice? posso usare value()?
    actionUtility = np.zeros(NUM_ACTIONS)
    actionUtility[otherAction] = 0
    actionUtility[(otherAction + 1) % NUM_ACTIONS] = 1
    actionUtility[(otherAction - 1) % NUM_ACTIONS] = -1

    #
    regretSum += actionUtility - actionUtility[myAction]

    return regretSum, strategySum

def train(iterations):
    regretSum = np.zeros(NUM_ACTIONS)
    strategySum = np.zeros(NUM_ACTIONS)

    for i in range(iterations):
        regretSum, strategySum = innerTrain(regretSum, strategySum, oppStrategy)
    return strategySum

def train2p(oiterations, iterations):
    strategySumP1 = np.zeros(NUM_ACTIONS)
    strategySumP2 = np.zeros(NUM_ACTIONS)

    for j in range(oiterations):
        oppStrategy = normalize(strategySumP2)
        regretSumP1 = np.zeros(NUM_ACTIONS)
        for i in range(iterations):
            regretSumP1, strategySumP1 = innerTrain(regretSumP1, strategySumP1, oppStrategy)

        oppStrategy = normalize(strategySumP1)
        regretSumP2 = np.zeros(NUM_ACTIONS)
        for i in range(iterations):
            regretSumP2, strategySumP2 = innerTrain(regretSumP2, strategySumP2, oppStrategy)

    return strategySumP1, strategySumP2

s1, s2 = train2p(20, 10000)

oppStrategy = np.zeros(3)

scelte = ['sasso', 'carta', 'forbice']

print('si giocano 6 partite in totale')

for i in range(6)
    a = input('inserire la mossa', )
    if input() in scelte:
