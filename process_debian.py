import readPreflib
import mallows_soi as mal
import MetropolisRunner
import numpy as np
# import LuBout

candidates, length_counts, votes = readPreflib.soiInputwithWeights("data_input/ED-debian-2002.soi")

total_votes = 1.0 * sum(length_counts.values())

length_probs = []

for i in range(1,len(length_counts.values())+1):
    length_probs.append(length_counts[i] / total_votes)
    
print(length_probs)

print(candidates)

# print(votes)

params = [np.asarray([1,2,3,4]), 0.5]
MetropolisRunner.metHastings(mal.costFunction, params, mal.generateCandidate, votes, 10, 0)