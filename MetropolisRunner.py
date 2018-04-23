# Migrating Current Thesis work to Python to quicken the development cycle
# Currrent state:
#       works just fine for nromal distribution floats
#       - make sure you send a float not an int
# Working on:
#       Need a way to generate the data
#       - prefmine Dlang code, also Lu & Boutillier 2014
#       Move things to new files probably
# done?
#       How to cache ktau?
#       was a huge improvement for floats
#       Mallows cost function seems wrong


import numpy as np
import functools
from random import shuffle
import mallows

# Reading in and formatting data for normal distribution
# normal_values[i, 0] = i, normal_values[i, 1] = i + std deviate
num_normals = 100
stddeviates = np.loadtxt("data.txt")
stddeviates = stddeviates[0: num_normals]
labels = np.arange(num_normals)
normal_values = np.column_stack((labels, stddeviates))

orderings = mallows.generateMallowsSet(100, 5, 0.5)

filewrite = []  # this is a placeholder for writing to a file


# @param params - list of tparams passed from metHastings
def gaussianCostFunction(params):
    return gaussianHelperFunction(params[0])


@functools.lru_cache(maxsize=128)
def gaussianHelperFunction(theta):
    loss = 0
    for i in range(len(normal_values)):
        temp = (theta * normal_values[i, 1]) - normal_values[i, 0]
        loss += temp * temp
    return loss


# Helper of the metropolis algorithm. Gnerates get new candidate params
# Previously known as 'wiggle'
def generateCandidate(o):
    if type(o) is float:
        # Add a random number
        return o + np.random.normal(0, 0.5)
    elif type(o) is list:
        mallows.generateOrdering(o)
        return o
        # do some number of swaps
    print(o)
    print("could not generate candidate")
    return -1


# How far off from the dataset is our current mu, phi?
def mallowsCostFunction(params):
    mu = params[0]
    phi = params[1]
    loss = 0
    for i in range(len(orderings)):
        loss += (phi * mallows.ktdistance(orderings[i], mu))
    return loss


# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, runs, burn_in):
    N = runs
    step = 0

    # open some file to print to ?
    
    # f = open("pythontest.txt", "w")

    while step != N:
        new_params = []
        new_params[:] = params

        for i in range(len(new_params)):
            new_params[i] = generateCandidate(new_params[i])

        # print(new_params)
        prev_cost = cost_model(params)
        new_cost = cost_model(new_params) + 1  # is this correct?

        # print(params, new_params)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost

        if alpha > u:
            params = list(new_params)
            prev_cost = new_cost

        if (step > burn_in):
            '''
            for val in params:
                if type(val) is float:
                    f.write(str("%.2f\n" % val))
                # need to make this order compatible
            '''
            print("Costs: ", "%.2f" % prev_cost, "%.2f" % new_cost)
            print("alpha, u: ", "%.4f" % alpha, "%.4f" % u)
            # tup = (params[0], params[1])
            # filewrite.append(tup)
        step += 1
    print("finished")
    # f.close()

if (True):
    starting_params = []
    starting_params.append(1.00)
    print("Initial cost:", gaussianCostFunction(starting_params))
    metHastings(gaussianCostFunction, starting_params, 10006, 10000)

if (False):
    a = [1, 2, 3, 4, 5]
    b = [3, 4, 1, 2, 5]
    # print("kt distance:", ktdistance(a, b))
    starting_params = [a, 1.0]
    print('initial mallows cost: ', mallowsCostFunction(starting_params))
    metHastings(mallowsCostFunction, starting_params, 1006, 1000)
    # wiggleOrderings(a)
    # print(a)
    for tup in filewrite:
        print(tup[0], tup[1])
