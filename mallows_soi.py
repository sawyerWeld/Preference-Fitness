# Mallows SOI functions having odd errors, even though the functions
# work fine in the eta vs kt dist jupyter notebook

# this is me pasting from the notebook to here 

import numpy as np
import itertools

# num = number of ranks
# N = length of each rank
def generateMallowsSet(num, N, eta, centroid=0):
    if centroid == 0:
        centroid = np.arange(N)
    list = []
    for _ in range(num):
        ord = np.arange(N)
        ord[0] = centroid[0]
        for i in range(1, N):
            ord[i] = centroid[i]
            j = i
            while (eta > np.random.uniform(0.0,1.0) and j >= 1):
                ord[j], ord[j-1] = ord[j-1], ord[j]
                j -= 1

        list.append(ord)
    return list

def np_index(array, value):
    return np.where(array==value)[0][0]

def ktdistanceSOI(a, b):
    pairs = itertools.combinations(a, 2)
    count = 0.0
    for i, j in pairs:
        #print('-----',i, j)
        half = False
        first = np_index(a, i) - np_index(a, j)
        #print(first, np_index(a, i))
        try:
            secnd = np_index(b, i) - np_index(b, j)
        except:
            half = True
            count += 0.5
        if not half and (first * secnd < 0):
            count += 1
    return count
