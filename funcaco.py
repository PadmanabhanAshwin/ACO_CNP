#Function to read instance file. 
import csv
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
from statistics import mean
import statistics

def importfile(filename):
    with open(filename) as filename:
        rows = csv.reader(filename)
        for i, row in enumerate(rows): 
            if i == 0:
                data = []
                data.append([i] + row[1:4])
            else: 
                #print(row)
                data.append([i] + row[1:4]) 
    return data

def isfeasible(startpoint, weights, knapsackcapacity):
    weight = sum([a*b for a, b in zip(startpoint, weights)])
    if weight>knapsackcapacity:
        return 0
    else: 
        return 1
def calcobj(startpoint, values):
    summ = sum([i*j for i, j in zip(startpoint, values)])
    return summ
def calcdist(startpoint, optimalgeno):
    diff = math.sqrt(sum([(a_i - b_i)**2 for a_i, b_i in zip(startpoint, optimalgeno)]))
    return diff

def setinitialprobability(data, knapsackcapacity):
    sumvalueperweight = 0
    for i in data:
        sumvalueperweight = sumvalueperweight + (int(i[1])/int(i[2]))
    res = []
    for i in data:
        res.append([i[0]]+ [(int(i[1])/(int(i[2])*sumvalueperweight))])
    return res

def updateneighbour(previousneighbourhood, presentknapsackcapacity, item):
    presentneightbourhood = copy.deepcopy(previousneighbourhood)
    removelist = []
    for i in previousneighbourhood.keys(): #previousneighbourhood is dict of { index:  [value, weight]} i in index here
        if presentknapsackcapacity < int(presentneightbourhood[i][1]):
            removelist.append(i)
    if item not in removelist: 
        removelist.append(item) 
    for i in removelist:
        del presentneightbourhood[i]
    return presentneightbourhood

def generatetransitionmatrix(presentneigh, tau, mu, alpha = 3, beta = 2 ):
    expresssum = 0
    for i in presentneigh.keys():
        expresssum = expresssum + ((tau[i]**alpha)*(mu[i]**beta))

    probmatrix = {
                    i: ((tau[i]**alpha)*(mu[i]**beta))/expresssum for i in presentneigh.keys()
                 }
    return probmatrix

def sampleitem(probmatrix):
    rand_val = random.random()
    total = 0
    for k, v in probmatrix.items():
        total += v
        if rand_val <= total:
            return k
    assert False, 'unreachable'

def updatephero(resofkants, tau, globalprofit):
    for i in resofkants:
        z = resofkants[i][0]
        deltatau = (1/(1+((globalprofit- z)/globalprofit)))
        for j in resofkants[i][1].keys():
            tau[j] = tau[j] + deltatau
    return tau

def evaporate(tau, rho):
    for i in tau.keys():
        tau[i] = max(0.05, tau[i]*rho)
    return tau

def normalize(probmat):
    summ = 0
    for i in probmat:
        summ = summ+ probmat[i]
    for i in probmat:
        probmat[i] = probmat[i]/summ
    return probmat

def generateoptimalgenotype(optimallist, len):
    res = [0 for i in range(len)]
    for i in optimallist:
        res[i] = 1
    return res

def aco(iterations, neighbourhood, knapsackcapacity, numants, probmatrix, tau , mu, alpha, beta):
    #random.seed(1)   WORKING SEED
    #seed = seed + 1
    iternumber = 0
    globalprofit = -1
    globaltrack= []
    globalsample = {}

    while iternumber < iterations:
        presentneigh = neighbourhood
        presentknapsackcapacity = knapsackcapacity
        resofkants = {}
        #print("Iteration Number: ", iternumber)
        antprofit = -1
        antsample = {}

        for ant in range(numants):
            localprofit = 0
            solutionset = {}
            while (presentknapsackcapacity>0) and ( len(presentneigh.keys()) > 0 ):
                presentkeys = presentneigh.keys()
                #print("Length of present neighbours= ", len(presentneigh))
                probmat = dict((k, probmatrix[k]) for k in presentkeys if k in probmatrix)
                probmat = normalize(probmat)

                item = sampleitem(probmat)
                #print("Item placed in knapsack is = ", item)
                solutionset.update({item: presentneigh[item]})
                presentknapsackcapacity = presentknapsackcapacity - presentneigh[item][1]
                localprofit = localprofit + presentneigh[item][0] 
                presentneigh = updateneighbour(presentneigh, presentknapsackcapacity, item)
                #print("Length of presentneighbour after placing item in knapsack - ", len(presentneigh))
                #print("Local profit is: ", localprofit)

            if localprofit > antprofit:
                antprofit = localprofit 
                antsample = solutionset
                #print("Ant profit updated to ", antprofit)

            resofkants.update({ ant: [ localprofit , solutionset]})

        if antprofit > globalprofit:
            #print("Global Profit updated to ", globalprofit)
            globalprofit = antprofit
            globalsample = antsample
            globaltrack.append(globalprofit)
        
        tau = updatephero(resofkants, tau, globalprofit)
        probmatrix = generatetransitionmatrix(neighbourhood, tau, mu, alpha, beta)
        iternumber = iternumber + 1

    print("alpha =", alpha, "beta =",  beta, "Global Best =  " , globalprofit)
    return [globalprofit, globalsample]

#function that "CALLS FUNCTION GA" and plots contours. 
def getcountour(alpharange, betarange, binsize, iterations, neighbourhood, knapsackcapacity, numants, probmatrix, tau, mu):
    #Crossoverrate in x axis:
    xlist = np.linspace(alpharange[0], alpharange[1], binsize)
    # Mutation rate in y axis:
    ylist = np.linspace(betarange[0], betarange[1], binsize)
    X, Y = np.meshgrid(xlist, ylist)

    fullz = []
    for i in xlist: 
        a1 = []
        for j in ylist:
            res= aco(iterations, neighbourhood, knapsackcapacity, numants, probmatrix, tau, mu, i, j) 
            a1.append(res)
        fullz.append(a1)

    fig = plt.figure(figsize=(6,5))
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes([left, bottom, width, height])

    cp = ax.contour(X, Y, fullz)
    ax.clabel(cp, inline=True, 
            fontsize=10)
    ax.set_title('Contour_13_50_1000.csv')
    ax.set_xlabel('alpha')
    ax.set_ylabel('beta')
    plt.show()

def plotdistancefitness(res):
    dist = [i[0] for i in res]
    fitness = [i[1] for i in res]
    plt.scatter(dist, fitness, color = "red", marker = "*")
    plt.title("Fitness Distance Correlation: Sixth instance")
    plt.xlabel("Distance")
    plt.ylabel("Fitness")

def massagedatatoplot(res):
    #func.plotdistancefitness(res)
    reslist = []
    for i in res:
        for j in range(len(res[i])):
            reslist.append([i, res[i][j]])
    df=pd.DataFrame(reslist,columns=['StepNumber','Fitness'])
    return df

#calculate Fitness- Distance Correlation: 
def calcFDC(res):
    fitness =[i[1] for i in res]
    distance = [i[0] for i in res]
    avgfitness = mean(fitness)
    avgdistance = mean(distance)
    fdcsum = 0 
    for i in res:
        fdcsum = fdcsum + ((i[1] - avgfitness)*(i[0] - avgdistance))
    fdcsum = fdcsum/(len(res))
    fdcsum = fdcsum / (statistics.stdev(fitness)*statistics.stdev(distance))
    return fdcsum

def calcAutoCorrelation(res):
    fitness =[i[1] for i in res]
    avgfitness = mean(fitness)
    corrsum = 0
    corrdeno = 0 
    for i in range(len(res) - 1):
        corrsum = corrsum + ((fitness[i] - avgfitness)*(fitness[i+1] - avgfitness))
        corrdeno = corrdeno + ((fitness[i] - avgfitness)**2)
    autocorrelation = corrsum/corrdeno
    autocorrlen = 1/math.log(autocorrelation)
    return autocorrlen

def calcIC(schema):
    terrainchoice = ["01", "0-1", "10", "1-1","-10", "-11"]
    countdict = {i : 0 for i in terrainchoice}
    #finding the count for each case: 
    for i in range(len(schema)-1):
        case = schema[i] + schema[i+1]
        if case in countdict:
            countdict[case] = countdict[case] + 1
    #converting to probability:
    dicsum = sum(countdict.values())
    for i in countdict:
        countdict[i] = countdict[i]/dicsum
    icsum = 0 
    for i in countdict:
        if countdict[i] != 0:
            icsum = icsum + (countdict[i]* math.log(countdict[i], 6))
    icsum = -1*icsum
    return icsum

def calcDB(schema):
    terrainchoice = ["00", "-1-1", "11"]
    countdict = {i : 0 for i in terrainchoice}
    #finding the count for each case: 
    for i in range(len(schema)-1):
        case = schema[i] + schema[i+1]
        if case in countdict:
            countdict[case] = countdict[case] + 1
    #converting to probability:
    dicsum = sum(countdict.values())
    for i in countdict:
        countdict[i] = countdict[i]/dicsum
    icsum = 0 
    for i in countdict:
        if countdict[i] != 0:
            icsum = icsum + (countdict[i]* math.log(countdict[i], 3))
    icsum = -1*icsum
    return icsum

def schemify(res):
    schema = []
    epsilon = 20
    fitness = [i[1] for i in res]
    for i in range(len(fitness) - 1):
        if ((fitness[i+1] - fitness[i]) > epsilon):
            schema.append("1")
        elif ((fitness[i+1] - fitness[i]) <= epsilon) and ((fitness[i+1] - fitness[i]) >= (-1*epsilon)) :
            schema.append("0")
        else:
            schema.append("-1")
    return schema

#Finding partial information content. 
def editscheme(schema):
    compressschema = []
    schemaedit = []
    for i in range(len(schema)):
        print(i)
        if(schema[i] != "0"):
            schemaedit.append(schema[i])

    for i in range(len(schemaedit) - 1):
        if ((schemaedit[i] == "1") and (schemaedit[i+1] == "-1")) or ((schemaedit[i] == "-1") and (schemaedit[i+1] == "1")):
        #if (schema[i]!=schema[i+1]):
            compressschema.append(schemaedit[i])
    if (schemaedit[-1] == "1"):
        compressschema.append(schemaedit[-1])
    return compressschema