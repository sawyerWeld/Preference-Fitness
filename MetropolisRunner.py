import numpy as np
import functools
from random import shuffle
import mallows
import gauss

filewrite = []  # this is a placeholder for writing to a file

# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, gen_candidate, dataset, runs, burn_in):
    N = runs
    step = 0

    while step < N:
        new_params = list(params)

        # Set the values of the new candidate
        new_params = gen_candidate(new_params)

        prev_cost = cost_model(params, dataset)
        new_cost = cost_model(new_params, dataset)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost

        print('cur', params[0], prev_cost)
        print('new', new_params[0], new_cost)
        print('alpha', alpha)

        if alpha > u:
            params = list(new_params)
            prev_cost = new_cost

        if (step > burn_in):
            tup = tuple(params)
            filewrite.append(tup)

        

        step += 1
    print("finished metropolis process")


def run_gaussian():
    # Reading in and formatting data for normal distribution
    # normal_values[i, 0] = i, normal_values[i, 1] = i + std deviate
    num_normals = 100
    stddeviates = np.loadtxt("data.txt")
    stddeviates = stddeviates[0: num_normals]
    labels = np.arange(num_normals)
    normal_values = np.column_stack((labels, stddeviates))

    starting_params = [1.00]
    print("Initial cost:", gauss.costFunction(starting_params, normal_values))
    metHastings(gauss.costFunction, starting_params, gauss.genCandidate, normal_values, 10006, 1000)
    with open('estimate_data.txt', 'w') as file:
        for tup in filewrite:
            for val in tup:
                file.write(str(val) + '\n')
    print('finished writing to file')


def run_mallows():
    order_length = 5
    orderings = mallows.generateMallowsSet(2, order_length, 0.5)
    a = list(range(1,order_length+1))
    # print(orderings)
    starting_params = [a, 1.0]
    print('initial mallows cost: ', mallows.costFunction(starting_params, orderings))
    metHastings(mallows.costFunction, starting_params, mallows.genCandidate, orderings, 10, -1)
    with open('mallows_data.txt', 'w') as file:
        for tup in filewrite:
            file.write(str(tup[0]) + '\n')
    print('finished writing to file')

# run_gaussian()
run_mallows()