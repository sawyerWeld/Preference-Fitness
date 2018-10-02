# Functions for finding the optimal set of plackett-luce weights for a given dataset

import random
import numpy as np

def initialWeights(N=5, mode='random', data=None):
    if mode == 'random':
        weights = np.zeros(N)
        for i in range(N):
            weights[i] = np.random.uniform()
        s = np.sum(weights)
        for i in range(N):
            weights[i] = weights[i] / s
        return weights
    elif mode == 'mode2':
        return defineWeightsProportionately(N, data)
    else:
        print('Mode', mode, 'is not a valid mode')

# Here is my attempted method:
# Sum the rank that each alternative received in each ordering
# let D_i = the ith ordering in our dataset
# let α_ni = the ranking alternative n in D_i
# sums[n] = [ sum{i=0,i=|D|}(α_ni) for all i ]
# let inverted = (1 / sums)
# weights = L2 norm of inverted
def defineWeightsProportionately(N, dataset):
    sums = np.zeros(N)
    for ranking in dataset:
        for i in range(len(ranking)):
            place = ranking[i]
            sums[place] += i + 1
    sums = normalize(sums)
    return sums

def normalize(vector):
    scale = 1.0 / np.sum(vector)
    return vector * scale

def uniformRandomDataset(N, nEntries):
    li = []
    for i in range(nEntries):
        arr = np.arange(N)
        np.random.shuffle(arr)
        li.append(arr)
    return li

# P(≻|W) ∝ Σ{≻ᵢ∈≻}Σ{j=[0,N)}log(Wⱼ/Σ{k[j,N)}Wₖ)
def costFunction(params, dataset):
    weights = params
    data = dataset
    N = len(weights)
    # Σ{≻ᵢ∈≻}
    probability = 0
    for succ in data:
        # Σ{j=[0,N)}
        partial_sum = 0
        for j in range(N-1):
            # log(Wⱼ/Σ{k[j,N)}Wₖ)
            numer = weights[j]
            # Σ{k[j,N)Wₖ}
            denom = sum(succ[j:N])
            partial_sum += np.log(numer / denom)
        probability += partial_sum
    return probability

def preflibSOIcost(params, dataset):
    # Add the number of occurances to the params
    # Perhaps a tuple?
    # (num_occurances, [weights])
    # Or even how it is read in
    # [num_occurances,v1,v2,...,vn]
    pass

def genCandidateNormal(weights):
    N = len(weights)
    chosen_index = random.randint(0,N-1)
    # This number here probably needs adjusting
    # σ ∝ N
    delta = np.random.normal(0, 1.0)
    prev = weights[chosen_index]
    new = delta + prev
    weights[chosen_index] = new if new > 0 else abs(delta)
    weights = normalize(weights)
    # print(sum(weights))
    return weights

# Transfer some mass from one alternative, j, to another, i
# The limit on mass transfered = Δ'(Wᵢ→Wⱼ) = Argmin(Wᵢ,1-Wⱼ)
# The mass transfered = Δ = U(0,αΔ') where α is a parameter
# indicating the aggresiveness of the transfer
def genCandidateTransfer(weights, aggresiveness = 0.05):
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
    return w
