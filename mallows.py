# Helper function for MetropolisRunner

import numpy as np
import itertools

# Kendall Tau disntace for Strict-Order Incomplete data
# If rank1 has {a > b} and rank2 has {b > a}, add 1
# If rank1 has {a > b} and rank2 has {a > b}, add 0
# If rank1 has {a > b} and rank2 has no info on the 
# relationship between a and b, add 0.5. 
def ktdistanceSOI(a, b):
    pairs = itertools.combinations(a, 2)
    count = 0.0
    for i, j in pairs:
        half = False
        first = a.index(i) - a.index(j)
        try:
            secnd = b.index(j) - b.index(j)
        except:
            half = True
            count += 0.5
        if not half and (first * secnd < 0):
            count += 1
    return count


def genCandidate(params):
    mu = params
    return generateOrdering(mu)


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


# Kendall Tau distance from ordering a to b or visaversa
# Assumes complete orderings from 0:N
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


# How far off from the dataset is our current mu, phi?
def costFunction(params, dataset):
    orderings = dataset
    mu = params
    loss = 0
    for i in range(len(orderings)):
        loss += ktdistance(orderings[i], mu) # * phi
        # Simply multiplying by phi does not make sense
        # I got it from some piece of literature, but of course it makes
        # the optimal phi approach 0
    return loss


def costFunctionSOI(params, dataset):
    loss = 0
    data = dataset
    mu = params
    for num_occurances, order in data:
        loss += ktdistance(order, mu) * num_occurances
    return loss

import readPreflib

candidates, data = readPreflib.readinSOIwfreqs('analysis/EDTest.soi')
print(costFunctionSOI([1,2], data))


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

# centroid = [3, 4, 1, 2, 5]
# print(generateMallowsSet(10,5,0.1))

