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


# Generates a new candidate given current ordering
def generateOrdering(order):
    # A do()while{} would work better here, not sure how in python
    tuning_parameter = 0.5
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    while (np.random.uniform(0.0, 1.0) >= tuning_parameter):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
        # swap two random ones


# Generate a set of mallows orderings
# num is how many orderings
# N is how long each is
# eta is acceptance param in range [0.0, 1.0)
def generateMallowsSet(num, N, eta, centroid = 0):
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

# print(generateMallowsSet(10,5,0.5))

