# Helper function for MetropolisRunner

import numpy as np
import itertools


def generateOrdering(order):
    # A do()while{} would work better here, not sure how in python
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    tuning_parameter = 0.75
    while (tuning_parameter <= np.random.uniform(0.0, 1.0)):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
        # swap two random ones

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