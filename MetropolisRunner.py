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

orderings = mallows.generateMallowsSet(100, 5, 0.1)

filewrite = []  # this is a placeholder for writing to a file


# params - list of params passed from metHastings
def gaussianCostFunction(params):
    return gaussianHelperFunction(params[0])

def generateGauss(input):
    return input + np.random.normal(0, 0.5)

# used by the cost function
@functools.lru_cache(maxsize=128)
def gaussianHelperFunction(theta):
    loss = 0
    for i in range(len(normal_values)):
        temp = (theta * normal_values[i, 1]) - normal_values[i, 0]
        loss += temp * temp
    return loss


# How far off from the dataset is our current mu, phi?
def mallowsCostFunction(params):
    mu = params[0]
    phi = params[1]
    loss = 0
    for i in range(len(orderings)):
        loss += mallows.ktdistance(orderings[i], mu) * phi
    return loss


# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, gen_candidate, runs, burn_in):
    N = runs
    step = 0

    while step != N:
        new_params = []
        new_params[:] = params

        # Set the values of the new candidate
        new_params = gen_candidate(new_params)

        prev_cost = cost_model(params)
        new_cost = cost_model(new_params)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost

        if alpha > u:
            params = list(new_params)
            prev_cost = new_cost

        if (step > burn_in):
            # print("Costs: ", "%.2f" % prev_cost, "%.2f" % new_cost)
            # print("alpha, u: ", "%.4f" % alpha, "%.4f" % u)
            tup = tuple(params)
            # print(tup)
            filewrite.append(tup)
        step += 1
    print("finished metropolis process")


def run_gaussian():
    starting_params = []
    starting_params.append(1.00)
    print("Initial cost:", gaussianCostFunction(starting_params))
    metHastings(gaussianCostFunction, starting_params, generateGauss, 10006, 1000)
    with open('estimate_data.txt', 'w') as file:
        for tup in filewrite:
            for val in tup:
                file.write(str(val) + '\n')
    print('finished writing to file')


def run_mallows():
    a = [1, 2, 3]
    start = []
    start = list(a)
    b = [3, 4, 1, 2, 5]
    starting_params = [a, 1.0]
    print('initial mallows cost: ', mallowsCostFunction(starting_params))
    metHastings(mallowsCostFunction, starting_params, mallows.mallowsCandidate, 1000, 100)
    with open('mallows_data.txt', 'w') as file:
        for tup in filewrite:
            file.write(str(tup[1]) + '\n')
    print('finished writing to file')

# run_gaussian()
run_mallows()