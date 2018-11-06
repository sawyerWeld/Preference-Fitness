import readPreflib
import mallows_soi as mal
import MetropolisRunner
import numpy as np
import plackettluce as pl
import math
# import LuBout

candidates, length_counts, votes = readPreflib.soiInputwithWeights("data_input/ED-debian-2002.soi")

total_votes = 1.0 * sum(length_counts.values())

length_probs = []

for i in range(1,len(length_counts.values())+1):
    length_probs.append(length_counts[i] / total_votes)
    
print(length_probs)

print(candidates)

def findMallows():
    params = [np.asarray([1,2,3,4]), 0.5]
    return MetropolisRunner.metHastings(mal.costFunction, params, mal.generateCandidate, votes, 1000, 0)

def findPlackett():
    initial = pl.initialWeights(N = 4)
    return MetropolisRunner.metHastings(pl.costFunction, initial, pl.genCandidateTransfer, votes, 1000, 0)

findPlackett()

def p_mallows(r, params):
    sigma, phi = params
    return mal.P(r, sigma, phi)

def p_plackett(r, params):
    weights = params
    return pl.prob_ranking(r, weights)

print(votes)

def findDivergence(votes, mallows_params, pl_params):
    kl_divergence = 0
    for tup in votes:
        num_occurances, r = tup
        Q = p_mallows(r, mallows_params)
        P = p_plackett(r, pl_params)
        kl_divergence += num_occurances * (Q * math.log(Q / P))
    return kl_divergence

print(findDivergence(votes, findMallows(), findPlackett()))