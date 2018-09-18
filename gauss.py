# Helper Functions for gaussian distribution param estimation

import functools
import numpy as np

# There may be a better way to handle setting the global dataset
# I only need to do this for cacheing reasons
dataset_defined = False
dataset = -1

# params - list of params passed from metHastings
def costFunction(params, data):
    global dataset
    if not dataset_defined:
        dataset = data
    return gaussianHelperFunction(params[0])

def genCandidate(num):
    return [num[0] + np.random.normal(0, 0.5)]

# used by the cost function
@functools.lru_cache(maxsize=128)
def gaussianHelperFunction(theta):
    normal_values = dataset
    loss = 0
    for i in range(len(normal_values)):
        temp = (theta * normal_values[i, 1]) - normal_values[i, 0]
        loss += temp * temp
    return loss