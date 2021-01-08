# pairwise.py

# The goal of this class is to take a batch of preferences and return either
# a matrix of their pairwise probabilities or a flattened vector of them

import readPreflib as pref
import numpy as np
import math

# returns occurance matrix
def pairwise_matrix_singular(vote):
    n = len(vote)
    occurance_matrix = np.full(shape = (n,n), dtype = int, fill_value = 0)
    
    for i, v in enumerate(vote):
        if v == 0:
            continue
        # list of alts that the current alt is better than
        better_than = [i+1 for i in range(n)]
        before = vote[:i+1]
        for b in before:
            better_than.remove(b)
        for p in better_than:
            occurance_matrix[v-1][p-1] = 1
            occurance_matrix[p-1][v-1] = -1
    return occurance_matrix

# Converts an upper triangular matrix to a vector
def matrix_to_vec(matrix):
    vec = []
    n = len(matrix[0])
    vec_length = n * (n-1) / 2
    offset = 1
    for inner in matrix:
        vec.extend(inner[offset:])
        offset += 1
    return np.array(vec)

def vec_to_matrix(vec_):
    data_type = vec_.dtype
    vec = list(vec_)
    m = len(vec)
    n = math.floor(math.sqrt(2*m))
    prob_matrix = np.full(shape = (n+1,n+1), dtype = data_type, fill_value = 0)
    row_offset = 1
    for row in prob_matrix:
        for i in range(row_offset,n+1):
            row[i] = vec.pop(0)
        row_offset += 1
    return prob_matrix

# Note as I write thesis: this is the one that gets used
def process_vote(vote):
    mat = pairwise_matrix_singular(vote)
    # print(mat)
    return matrix_to_vec(mat)


if __name__ == '__main__':
    print('Executing main thread in pairwise.py')
    np.set_printoptions(precision=3)
    candidates, votes = pref.readinSOIwfreqs('data_in/Practice/ED-02-Logo.soi')
    a = np.array([3, 2, 1, 0, 0, 0])
    vec = process_vote(a)
    print(vec)
    print('mat now')
    #print(matrix_to_vec(vec))
    # prob = pairwise_from_votes(votes[0], len(candidates))
    # print(prob)
    # vec = matrix_to_vec(prob)
    # print(vec)
    print(vec_to_matrix(vec))
    print(process_vote(a))