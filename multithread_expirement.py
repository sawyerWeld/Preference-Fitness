# learning how to use pools in python

from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
import itertools
import readPreflib

def square(x):  
    # calculate the square of the value of x
    return x*x


def getWeight(num, weights):
    return weights[num-1]

def f(tup):
    return probPlackett(tup[0], tup[1])

def probPlackett(tup, weights):
    num, r = tup
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


def plackettCost(params, dataset, lengths):
    weights = params
    cost = 0
    for tup in dataset:
        num_occurances, r = tup
        cost += lengths[len(r)-1] * num_occurances * probPlackett(r, weights)
    return cost


def plackettCostMulti(params, dataset, lengths):
    weights = params
    cost = 0
    costs = []

    num_occurances_list = [i[0] for i in dataset]
    votes_list = [i[1] for i in dataset] 

    pool = ThreadPool(4)



    # costs = pool.map(probPlackett, dataset, itertools.repeat(weights, len(dataset)))

    list_of_params = list(itertools.repeat(weights, len(dataset)))
    # print(list_of_params)

    # res = pool.map(probPlackett, dataset, list(itertools.repeat(weights, len(dataset))))
    res = list_of_params

    pool.close() 
    pool.join() 
   
   
    return res

candidates, length_counts, votes = readPreflib.soiInputwithWeights('data_input/ED-debian-2002.soi')

plackettCostMulti([0.25,0.25,0.4,0.1], votes, length_counts)

# def add(x, y):
#     return x + y

# a = [1, 2, 3]
# res = map(add, a, itertools.repeat(2, len(a)))
# print(list(res))


# print(probPlackett((3, [1,2,3]), [0.3,0.4,0.3]))


with ThreadPool(processes=4) as pool:
    print(pool.map(square, range(10)))

    for i in pool.imap_unordered(square, range(10)):
        print(i)

    res = pool.apply_async(f, list(votes))
    print(res.get(timeout=1))
