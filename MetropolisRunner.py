# Migrating Current Thesis work to Python to quicken the development cycle
# Currrent state:
#       works just fine for nromal distribution floats
#       - make sure you send a float not an int
# Working on:
#       Need a way to generate the data
#       - prefmine Dlang code, also Lu & Boutillier 2014
#       Move things to new files probably
#       How to cache ktau?
#       Mallows cost function seems wrong


import numpy as np
import itertools
import functools
from random import shuffle

# Reading in and formatting data for normal distribution
# normal_values[i, 0] = i, normal_values[i, 1] = i + std deviate
num_normals = 100
stddeviates = np.loadtxt("data.txt")
stddeviates = stddeviates[0: num_normals]
labels = np.arange(num_normals)
normal_values = np.column_stack((labels, stddeviates))

# Creating list of orderings
# This is a RANDOM list of orderings, it is a placeholder
base_ordering = [1, 2, 3, 4, 5]
orderings = []
for i in range(100):
    new_ordering = base_ordering[:]
    shuffle(new_ordering)
    orderings.append(new_ordering)
orderings = np.asarray(orderings)


# @param params - list of params passed from metHastings
def gaussianCostFunction(params):
    return gaussianHelperFunction(params[0])


@functools.lru_cache(maxsize=128)
def gaussianHelperFunction(theta):
    loss = 0
    for i in range(len(normal_values)):
        temp = (theta * normal_values[i, 1]) - normal_values[i, 0]
        loss += temp * temp
    return loss


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


def wiggleOrderings(order):
    # A do()while{} would work better here, not sure how in python
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    tuning_parameter = 0.5
    while (tuning_parameter <= np.random.uniform(0.0, 1.0)):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
        # swap two random ones


# How far off from the dataset is our current mu, phi?
def mallowsCostFunction(params):
    mu = params[0]
    phi = params[1]
    loss = 0
    for i in range(len(orderings)):
        loss += np.exp(-1 * phi * ktdistance(orderings[i], mu))
    return loss


# Helper of the metropolis algorithm. Gnerates get new candidate params
# Previously known as 'wiggle'
def generateCandidate(o):
    if type(o) is float:
        # Add a random number
        return o + np.random.normal(0, 0.5)
    elif type(o) is list:
        wiggleOrderings(o)
        return o
        # do some number of swaps
    print(o)
    print("could not generate candidate")
    return -1


# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, runs, burn_in):
    N = runs
    step = 0

    # open some file to print to ?
    filewrite = []  # this is a placeholder for writing to a file
    f = open("pythontest.txt", "w")

    while step != N-1:
        new_params = []
        new_params[:] = params

        for i in range(len(new_params)):
            new_params[i] = generateCandidate(new_params[i])

        # print(new_params)
        prev_cost = cost_model(params)
        new_cost = cost_model(new_params) + 0.00000001

        # print(params, new_params)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost
        # print("Costs: ", "%.2f" % prev_cost, "%.2f" % new_cost)
        # print("u, alpha: ", "%.4f" % u, "%.4f" % alpha)

        if alpha > u:
            params = list(new_params)
            prev_cost = new_cost

        if (step > burn_in):
            for val in params:
                if type(val) is float:
                    f.write(str("%.2f\n" % val))
                # need to make this order compatible
        step += 1
    print("finished")
    f.close()


# starting_params = []
# starting_params.append(1.00)
# print("Initial cost:", gaussianCostFunction(starting_params))
# metHastings(gaussianCostFunction, starting_params, 10000, 2000)

a = [1, 2, 3, 4, 5]
b = [3, 4, 1, 2, 5]
# print("kt distance:", ktdistance(a, b))
starting_params = [b, 1.0]
print("initial mallows cost: ", mallowsCostFunction(starting_params))
metHastings(mallowsCostFunction, starting_params, 1000, 200)
wiggleOrderings(a)
print(a)
