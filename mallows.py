# Helper function for MetropolisRunner

import numpy as np
import itertools


# Kendall Tau distance from ordering a to b or visaversa
def ktdistance(a, b):
    if len(a) != len(b):
        return -1
    pairs = itertools.combinations(range(len(a)), 2)
    count = 0
    for i, j in pairs:
        first = a[i] - a[j]
        secnd = b[i] - b[j]
        if (first * secnd < 0):
            count += 1
    return count

def genCandidate(tup):
    order = tup[0]
    num = tup[1]
    new_order = generateOrdering(order)
    new_num = num + np.random.normal(0, 0.5)
    return ((new_order, new_num))

# Generates a new candidate given current ordering
def generateOrdering(order):
    # A do()while{} would work better here, not sure how in python
    tuning_parameter = 0.1
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    while (np.random.uniform(0.0, 1.0) >= tuning_parameter):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
        # swap two random ones
    return order

# How far off from the dataset is our current mu, phi?
def costFunction(params, dataset):
    orderings = dataset
    mu = params[0]
    phi = params[1]
    loss = 0
    for i in range(len(orderings)):
        loss += ktdistance(orderings[i], mu) # * phi
        # Simply multiplying by phi does not make sense
        # I got it from some piece of literature, but of course it makes
        # the optimal phi approach 0
    return loss

# Generate a set of mallows orderings
# num is how many orderings
# N is how long each is
# eta is acceptance param in range [0.0, 1.0)
# see Lu & Boutillier 2014
def generateMallowsSet(num, N, eta, centroid=0):
    if centroid == 0:
        centroid = np.arange(N)
    list = []
    for i in range(num):
        ord = np.arange(N)
        ord[0] = centroid[0]
        for i in range(1, N):
            ord[i] = centroid[i]
            for j in range(i, 0, -1):
                if eta > np.random.uniform(0.0, 1.0):
                    ord[j], ord[j-1] = ord[j-1], ord[j]
                else:
                    break
        list.append(ord)
    return list

centroid = [3, 4, 1, 2, 5]
# print(generateMallowsSet(10,5,0.1))

