import numpy as np
import functools
from random import shuffle
from tqdm import tqdm
import rankutils
import time
import mallows
import gauss
import plackettluce as pl
import readPreflib


filewrite = []  # this is a placeholder for writing to a file

# cost_model - which cost model to iterate over
# params     - starting params to iterate from
# runs       - how many times to iterate, includes burn in
# burn_in    - iterations not to record, necessary for markov chains
def metHastings(cost_model, params, gen_candidate, dataset, runs, burn_in):
    N = runs
    step = 0
    lowest_cost = 1000000000000 # How get max int in python?
    lowest_cost_params = None

    for step in tqdm(range(N)):
        # Set the values of the new candidate
        new_params = gen_candidate(params)
        
        prev_cost = cost_model(params, dataset)
        new_cost = cost_model(new_params, dataset)

        u = np.random.uniform(0, 1)
        alpha = prev_cost / new_cost

        # print(params, prev_cost)
        # print(new_params, new_cost)

        if alpha > u:
            # print( params, prev_cost, new_params, new_cost, alpha, u)
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
    return lowest_cost


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
    with open('data_output/estimate_data.txt', 'w') as file:
        for tup in filewrite:
            file.write(str(tup[0][0]) + '\n')
    print('Finished writing to file')


def run_mallows():
    order_length = 5
    orderings = mallows.generateMallowsSet(100, order_length, eta=0.99, centroid=[4,3,2,1,0])
    a = list(range(1,order_length+1))
    starting_params = a
    print('initial mallows cost: ', mallows.costFunction(starting_params, orderings))
    nEntries = 1000
    lowest = metHastings(mallows.costFunction, starting_params, mallows.genCandidate, orderings, nEntries, 0)
    #print('Phi = ', (lowest/nEntries)**(1/2))
    print('Number of swaps in best case:', lowest/nEntries)
    with open('data_output/mallows_data.txt', 'w') as file:
        file.write('Ordering' + '\t' + 'Cost' + '\n')
        for line in filewrite:
            ordering = ''.join(map(str, line[0]))
            file.write(ordering + '\t' + str(line[1]) + '\n')
    print('Finished writing to file')

run_mallows()

def run_plackettluce():
    # First step: Produce a set of weights as a starting param
    initial = pl.initialWeights(N = 5)
    data = pl.uniformRandomDataset(5, 100)
    print('initial P-L cost:', pl.costFunction(initial, data))
    metHastings(pl.costFunction, initial, pl.genCandidateTransfer, data, 10001, 5000)
    with open('data_output/PL-data.txt', 'w') as file:
        for i in tqdm(range(len(filewrite))):
            line = filewrite[i]
            rank = rankutils.listtostring(line[0], delim=' ')
            file.write(rank + '\t' + str(line[1]) + '\n')
    print('Finished writing to file')

def run_plackettluce_on_soi():
    initial = pl.initialWeights(N = 12)
    candidates, data = readPreflib.readinSOIdata('analysis/EDIreland.soi')
    print('initial P-L cost:', pl.costFunction(initial, data))
    metHastings(pl.costFunction, initial, pl.genCandidateTransfer, data, 2000, 1000)
    with open('data_output/PL-data-debian.txt', 'w') as file:
        for i in tqdm(range(len(filewrite))):
            line = filewrite[i]
            rank = rankutils.listtostring(line[0], delim=' ')
            file.write(rank + '\t' + str(line[1]) + '\n')
    print('Finished writing to file')

# run_plackettluce_on_soi()














