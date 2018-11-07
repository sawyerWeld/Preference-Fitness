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

def findMallowsSigma():
    params = np.asarray([1,2,3,4])
    return MetropolisRunner.metHastings(mal.costFunctionSigma, params, mal.generateOrdering, votes, 1000, 0)

def findMallowsPhi(sigma):
    params = [sigma, 1.0]
    return MetropolisRunner.metHastingsMax(mal.costFunction, params, mal.generateCandidatePhi, votes, 500)

def findMallows():
    params = [np.asarray([1,2,3,4]), 1.0]
    return MetropolisRunner.metHastingsMax(mal.costFunction, params, mal.generateCandidate, votes, 30000)

def findPlackett():
    initial = pl.initialWeights(N = 4)
    return MetropolisRunner.metHastings(pl.preflibSOIcost, initial, pl.genCandidateTransfer, votes, 1000, 0)

# max_params, greatest_cost, li = findMallows()
# print(max_params, greatest_cost)

print(findMallowsSigma())

# findPlackett()
# sigma = [2, 1, 3, 4] # findMallowsSigma()
# phi, cost, li = findMallowsPhi(sigma)
# print(phi, cost)
# print(li)

# np.savetxt('data_output/phi.csv', li, delimiter=',')


def p_mallows(r, params):
    sigma, phi = params
    return mal.P(r, sigma, phi)

def p_plackett(r, params):
    weights = params
    return pl.prob_ranking(r, weights)

# print(votes)

def findDivergence(votes, mallows_params, pl_params):
    kl_divergence = 0
    for tup in votes:
        num_occurances, r = tup
        Q = p_mallows(r, mallows_params)
        P = p_plackett(r, pl_params)
        print('Q,P',Q,P)
        kl_divergence += num_occurances * (Q * math.log(abs(Q / P)))
    return kl_divergence


    # PL doesnt return a probability, its a negative number
    # Mallows phi doesnt work right
    # Handly 0s in K-L divergence

# print(findDivergence(votes, findMallows(), findPlackett()))