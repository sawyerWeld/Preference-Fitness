import numpy as np
import functools
from random import shuffle
from tqdm import tqdm
import time
import mallows
import gauss
import plackettluce as pl


filewrite = []  # this is a placeholder for writing to a file

# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, gen_candidate, dataset, runs, burn_in):
    N = runs
    step = 0
    lowest_cost = 1000000000000
    lowest_cost_params = None

    for step in tqdm(range(N)):
        # Set the values of the new candidate
        new_params = gen_candidate(params)

        prev_cost = cost_model(params, dataset)
        new_cost = cost_model(new_params, dataset)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost

        if alpha > u:
            params = new_params
            prev_cost = new_cost

        if (step > burn_in):
            tup = [tuple(params), prev_cost]
            filewrite.append(tup)

        if prev_cost < lowest_cost:
            lowest_cost = prev_cost
            lowest_cost_params = params

        step += 1

    print('Minimum cost:', lowest_cost)
    print('~Best params:', lowest_cost_params)
    print("Finished metropolis process")


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
    metHastings(gauss.costFunction, starting_params, gauss.genCandidate, normal_values, 10000, 1000)
    with open('estimate_data.txt', 'w') as file:
        for tup in filewrite:
            file.write(str(tup[0][0]) + '\n')
    print('Finished writing to file')


def run_mallows():
    order_length = 5
    orderings = mallows.generateMallowsSet(100, order_length, 0.4, centroid=[4,3,2,1,0])
    a = list(range(1,order_length+1))
    # print(orderings)
    starting_params = [a, 1.0]
    print('initial mallows cost: ', mallows.costFunction(starting_params, orderings))
    metHastings(mallows.costFunction, starting_params, mallows.genCandidate, orderings, 100000, 1000)
    with open('mallows_data.txt', 'w') as file:
        for line in filewrite:
            ordering = ''.join(map(str, line[0][0]))
            file.write(ordering + '\t' + str(line[1]) + '\n')
    print('Finished writing to file')


def run_plackettluce():
    order_length = 10
    orderings = mallows.generateMallowsSet(100, order_length, 0.4, centroid=[9,8,7,6,5,4,3,2,1,0])
    a = [1,2,3,4,5,6,7,8,9]
    starting_params = [a]
    print('initial P-L cost: ', pl.costFunction([a], orderings))
    metHastings(pl.costFunction, starting_params, pl.genCandidate, orderings, 100000, 50000)
    with open('PL_data.txt', 'w') as file:
        for line in filewrite:
            ordering = ''.join(map(str, line[0][0]))
            file.write(ordering + '\t' + str(line[1]) + '\n')
    print('Finished writing to file')


# run_gaussian()
# run_mallows()
run_plackettluce()