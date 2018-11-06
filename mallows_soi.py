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

# This is the only kt distance SOI function that should be used, other are wrong
def ktdistanceSOI(a, b):
    # print('kt', a, b)
    unique_set =  np.unique(np.concatenate([a,b]))
    pairs = itertools.combinations(unique_set, 2)
    count = 0.0
    for i, j in pairs:
        # print(i, j,'-----', count)
        unknown = False
        try:
            first = np_index(a, i) - np_index(a, j)
            secnd = np_index(b, i) - np_index(b, j)
        except:
            unknown = True
            count += 0.5
        if not unknown and (first * secnd < 0):
            count += 1
    return count

# a = np.asarray([1,2,3])
# b = np.asarray([2,3,4])
# print(np.unique(np.concatenate([a,b])))
# print(ktdistanceSOI(a,b))

# Equation 2 from Lu & Boutillier 2014
# The probability of a given ranking given the central
# ranking, sigma, and the dispersion param phi
def P(r, sigma, phi):
    return (1.0 / Z(phi, len(r))) * (phi ** (ktdistanceSOI(r, sigma)))

# Equation 3 from Lu & Boutillier 2014
def Z(phi, m):
    product = 1
    for i in range(1, m):
        part = partial(phi, i)
        product *= part
    return product

def test_Z():
    ans = Z(2, 3)
    print(ans)
    # 1             | 1
    # 1 + 2         | 3
    # 1 + 2 + 4     | 7
    # 1 + 2 + 4 + 8 | 15
    # 1 * 3 * 7 * 15 = 315
    assert(ans == 315)
    print('Test Passed')

def test_P():
    r = np.asarray([1,2,3])
    sigma = np.asarray([1,3,2])
    phi = 1.5
    i = 0.25
    while i < 1.0:
        ans = P(r, sigma, i)
        print(i, ans)
        i += 0.25
    # print(ans)
    

    pass

# (1 + φ + φ^2 + ... + φ^i)
def partial(phi, i):
    li = np.arange(i)
    seq = map(lambda x: phi ** x, li)
    ans = 1.0 * np.sum(np.fromiter(seq, dtype=np.float))
    return ans

def costFunction(params, dataset):
    central_ranking, phi = params
    cost = 0
    for tup in dataset:
        num_occurances, r = tup
        cost += (num_occurances * P(r, central_ranking, phi))
    return cost

def generateOrdering(order):
    # A do()while{} would work better here, not sure how in python
    tuning_parameter = 0.3
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    while (np.random.uniform(0.0, 1.0) >= tuning_parameter):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
        # swap two random ones
    return order

def generateDispersion(phi):
    delta = np.random.uniform(-0.1,0.1)
    new = phi + delta
    while(new <= 0 or new > 1):
        delta = np.random.uniform(-0.1,0.1)
        new = phi + delta
    return new

def generateCandidate(params):
    central_ranking, phi = params
    new_ranking = generateOrdering(central_ranking)
    new_phi = generateDispersion(phi)
    return [new_ranking, new_phi]
