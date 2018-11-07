import numpy as np
import itertools
import math

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
    # return 1.0 / (Z(phi, len(r)-1)) * (phi ** (ktdistanceSOI(r, sigma)))
    norm = 1.0 / Z(phi, len(r)-1)
    also = math.exp(-1.0 * phi * ktdistanceSOI(r, sigma))
    return norm * also


# Equation 3 from Lu & Boutillier 2014
def Z(phi, m):
    product = 1
    for i in range(1, m):
        part = partial(phi, i)
        product *= part
    return product

# (1 + φ + φ^2 + ... + φ^i)
def partial_2(phi, i):
    li = np.arange(i)
    seq = map(lambda x: math.exp(-1.0 * phi * x), li)
    ans = 1.0 * np.sum(np.fromiter(seq, dtype=np.float))
    return ans

# rewrote partial to make sure i wasnt messing something up
# hard to debug lambdas
def partial(phi, i):
    total = 0
    for j in range(0,i):
        total += math.exp(j * -1 * phi)
    return total

def costFunction(params, dataset):
    central_ranking, phi = params
    cost = 0
    for tup in dataset:
        num_occurances, r = tup
        cost += (num_occurances * P(r, central_ranking, phi))
    return cost

# for finding only sigma
def costFunctionSigma(params, dataset):
    central_ranking = params
    cost = 0
    for tup in dataset:
        num_occurances, r = tup
        cost += num_occurances * ktdistanceSOI(central_ranking, r)
    return cost

def generateCandidatePhi(params):
    central_ranking, phi = params
    new_phi = generateDispersion(phi)
    return [central_ranking, new_phi]

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

# When using phi bounded by (0,1]
def generateDispersion_outdated(phi):
    delta = np.random.uniform(-0.1,0.1)
    new = phi + delta
    while(new <= 0 or new > 1):
        delta = np.random.uniform(-0.1,0.1)
        new = phi + delta
    return new

def generateDispersion(phi):
    t_p = 0.1 # tuning param
    delta = np.random.uniform(-1 * t_p,t_p)
    new = phi + delta
    while(new <= 0):
        delta = np.random.uniform(-1 * t_p,t_p)
        new = phi + delta
    return new

def generateCandidate(params):
    central_ranking, phi = params
    new_ranking = generateOrdering(central_ranking)
    new_phi = generateDispersion(phi)
    return [new_ranking, new_phi]

# test_P()