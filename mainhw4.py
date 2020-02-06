#%%
import csv
import funcaco as func
import random
import copy
import matplotlib.pyplot as pl
import pandas as pd
from random import sample
from random import randrange
from random import choice
import math
import seaborn as sns
from statistics import mean
import statistics

#%% Get data
datafilename = "sixthinstance.csv"
data = func.importfile(datafilename)

#%% System Parameters
knapsackcapacity = 997 #HARD-CODED
presentknapsackcapacity = knapsackcapacity

iterations = 20
numants = 10
rho= 0.2

neighbourhood = {i[0]: [int(i[1]), int(i[2]) ] for i in data }
presentneigh = copy.deepcopy(neighbourhood)
tau = {i[0]: 10 for i in data}
mu = {i[0]: ((int(i[1])*presentknapsackcapacity)/int(i[2])) for i in data}
alpha = 3
beta = 2

probmatrix= func.generatetransitionmatrix(presentneigh, tau, mu, alpha, beta)
presentprobmatrix = copy.deepcopy(probmatrix)
#%% Final optimal using Ant colony optimization code from last time (takes lesser time and much more robust than GA)
#Optimal is a list [optimalvalue, optimalsolution {id: [value, weight]}]
optimal = func.aco(iterations, neighbourhood, knapsackcapacity, numants, probmatrix, tau, mu, alpha, beta)
#optimalgeno = [1, len(data)] bool list
optimalgeno = func.generateoptimalgenotype(optimal[1], len(data))
#%% Model the random walks
#Generate a starting point: 
sampleprob = {i: 1/len(data) for i in range(len(data))} #uniform, probability you sammple a point. RW problem.
solutionset = {}
presentknapsackcapacity = knapsackcapacity
presentneigh = neighbourhood

while (presentknapsackcapacity>0) and ( len(presentneigh.keys()) > 0 ):
    presentkeys = presentneigh.keys()
    probmat = dict((k, sampleprob[k]) for k in presentkeys if k in sampleprob) #generate the probability if in presentkeys. 
    probmat = func.normalize(probmat)

    item = func.sampleitem(probmat)
    solutionset.update({item: presentneigh[item]})
    presentknapsackcapacity = presentknapsackcapacity - presentneigh[item][1]
    presentneigh = func.updateneighbour(presentneigh, presentknapsackcapacity, item)
maxrestarts = 70
restarts = 0
maxsteps = 30

res = {i : [] for i in range(maxsteps)}   

while(restarts<maxrestarts):
    steps = 0
    weights = [int(i[2]) for i in data]
    values = [int(i[1]) for i in data ]
    print(restarts)
    if restarts == 0:
        startpoint = copy.deepcopy(optimalgeno)
        presentpoint = startpoint
        res[steps].append(func.calcobj(startpoint, values))
        #res.append([func.calcdist(presentpoint, optimalgeno), func.calcobj(startpoint, values)])
    else:
        startpoint = func.generateoptimalgenotype(solutionset, len(data))
        presentpoint = startpoint
        res[steps].append(func.calcobj(startpoint, values))

    while(steps<maxsteps):
        paths = []
        for i in range(len(presentpoint)):
            temppresentpoint = copy.deepcopy(presentpoint)
            if temppresentpoint[i] == 0:
                temppresentpoint[i] = 1
            else:
                temppresentpoint[i] = 0
            if func.isfeasible(temppresentpoint, weights, knapsackcapacity):        
                paths.append(i) #flipping this bit will result in a valid solution
        smp = random.choice(paths)
        if presentpoint[smp] == 0: 
            presentpoint[smp] = 1
        else: 
            presentpoint[smp] = 0
        res[steps].append(func.calcobj(startpoint, values))
        #res.append([func.calcdist(presentpoint, optimalgeno), func.calcobj(startpoint, values)])
        steps = steps+1
    restarts = restarts + 1

df = func.massagedatatoplot(res)
sns.relplot(x="StepNumber", y="Fitness", kind="line", data=df)

#%%
