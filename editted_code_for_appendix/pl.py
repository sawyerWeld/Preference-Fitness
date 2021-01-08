# Converted from IPython Notebook to .py file for inclusion in thesis

import numpy as np
from tqdm import tqdm_notebook
import math
import random
import itertools
import readPreflib
import metropolis

def probPlackett(r, weights):
    product = 1
    for i in range(0,len(r)):
        numer = getWeight(r[i],weights)
        denom = 0
        for j in range(i,len(r)):
            denom += getWeight(r[j],weights)
        if denom == 0:
            product *= numer
        else:
            product *= (1.0 * numer) / denom
    return product

# alternatives are 1-indexed in the preflib data
# kept forgetting this so made it a seperate method
def getWeight(num, weights):
    return weights[num-1]

def plackettCostComplete(params, dataset, lengths):
    weights = params
    for tup in dataset:
        num_occurances, r = tup
        cost += num_occurances * probPlackett(r, weights)
    return cost

# Two ways of initializing weights
def randomWeights(N):
    weights = np.zeros(N)
    for i in range(N):
        weights[i] = np.random.uniform()
        s = np.sum(weights)
        for i in range(N):
            weights[i] = weights[i] / s
    return weights

def uniformWeights(N):
    weights = np.zeros(N)
    for i in range(N):
        weights[i] = 1.0 / N
    return weights

# Generating new weight vector
def transferMass(weights, aggresiveness = 0.05):
    w = list(weights)
    N = len(w)
    index1 = random.randint(0,N-1)
    index2 = random.randint(0,N-1)
    while (index2 == index1):
        index2 = random.randint(0,N-1)

    initial1 = w[index1]
    initial2 = w[index2]
    limit  = min(initial1, 1.0 - initial2)
    delta = np.random.uniform(0.0, limit * aggresiveness)
    w[index1] = initial1 - delta
    w[index2] = initial2 + delta
    # print(weights, 'and', w)
    return np.asarray(w)

def runPL(rankings, n_runs, lengths_vector, complete = False):
    lengths = getLengthProbs(lengths_vector)
    num_alternatives = max(list(lengths_vector.keys()))
    print(lengths)
    if complete:
        num_alternatives = list(lengths_vector.keys())[0]
    initial_weights = randomWeights(num_alternatives)
    print('initial weights', initial_weights)
    costfunc = plackettCost
    if complete:
        costfunc = plackettCostComplete
    params, cost = metropolis.maximize(costfunc, lengths, initial_weights, transferMass, rankings, n_runs)
    return params
    
# Save output
import pickle
pickle.dump(params, open('pickle/plexample.p','wb'))