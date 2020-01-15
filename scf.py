from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import numpy as np
import random

sasso,carta,forbice = 0,1,2
NUM_ACTIONS = 3
oppStrategy = np.random.rand(NUM_ACTIONS)
oppStrategy = oppStrategy / np.sum(oppStrategy)

x= ["s", "c", "f"]
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

        print(normalize(strategySumP1), normalize(strategySumP2))
    return strategySumP1, strategySumP2

print("Sfida secolare tra due pc, di cui uno è stupido e gioca inizialmente con probabilità 0.4-0.3-0.3 rispettivamente sasso,carta o forbice")
print(x,x)
s1, s2 = train2p(20, 10000)

vvv = []
for j in range(200):
    vv = 0
    for i in range(100):
        #strategy = np.array([0,1,0])
        #strategy = getStrategy(regretSum)
        myAction = getAction(normalize(s1))
        otherAction = getAction(normalize(s2))
        vv += value(myAction, otherAction)
    vvv.append(vv)

plot(sorted(vvv))
print(np.mean(vvv), np.median(vvv))

show()
