#Converted from IPython Notebook to .py file for inclusion in thesis



import import_ipynb
from Mallows_Notebook import *
from PL_Notebook import *
import metropolis
import math
from tqdm import tqdm_notebook
import itertools


# Finds all files with 10 or less alternatives
u10 = []
for file in soi_files:
    cands, lengths, num_votes, votes = readPreflib.soiInputwithNumVotes(file)
    complete = True
    if len(cands) != len(lengths.keys()):
        complete = False
    if len(cands) < 10 and complete:
        u10.append(file)

list_of_votes = []
mallows_params = []
pl_params = []
nruns = 5_000 # made smaller for faster testing, more runs were used in publication 5k takes ~3 hours

print('Projected Time =',143/50.0 * nruns,'seconds, which is ~', 30/1000.0 * nruns, 'minutes')
for file in tqdm_notebook(u10, desc = 'All Files'):
    # print(file)
    cands, lengths, num_votes, votes = readPreflib.soiInputwithNumVotes(file)
    num_alternatives = len(cands)
    #print(num_alternatives)
    #print(num_votes)
    #print(list(lengths.keys()))
    list_of_votes.append((num_votes, lengths, votes))
    # print(list_of_votes[0])
    p_mal = runMallows(votes, num_alternatives, nruns, lengths)
    mallows_params.append(p_mal)
    p_pl = runPL(votes, nruns, lengths)
    pl_params.append(p_pl)


# save parameter sets to disk
pickle.dump([mallows_params, pl_params], open('pickle/u10_28_5k.p','wb'))

# Make list of all possible top orderings of size n or less
# Referred to as F(n) in text

def all_possible_votes(n):
    all_votes = []
    for i in range(1,n+1):
        sub = list(itertools.permutations(range(1,n+1),i))
        for p in sub:
            all_votes.append(p)
    return all_votes

#len(all_possible_votes(8)) = 109600

# Mark wether or not a vote is in our dataset
_,_,temp = list_of_votes[0]
known = [tuple(x) for x in list(zip(*temp))[1]]

import collections
def default_to_sorted(dictdict):
    lens_dict = dictdict
    od = collections.OrderedDict(sorted(lens_dict.items()))
    if 0 in od:
        del(od[0])
    return od

# Define squared difference
def squaredDif(a, b):
    return (a - b)**2

table = []
col_names = ['Number_Votes','Mallow\'s_Divergence','Plackett-Luce_Divergence']

# Iterate over all votes, finding the squared dif of E_i and T_i

for i in tqdm_notebook(range(len(list_of_votes))):
    num_votes, lengths, votes = list_of_votes[i]
    print(num_votes)
    lengths = default_to_sorted(lengths)
    num_alternatives = len(lengths)
    sigma, phi = mallows_params[i]
    pl_weights = pl_params[i]
    
    delta_mallows = 0
    delta_plackett = 0
       
    freq_list = list(zip(*votes))[0]
    known_votes = [tuple(x) for x in list(zip(*votes))[1]]
    vote_in = 0
    for vote in tqdm_notebook(all_possible_votes(num_alternatives)):
        if (vote in known_votes):
            vote_in += 1
            index = known_votes.index(vote)
            num_occurances = freq_list[index]
            
            empirical = num_occurances / num_votes
            mallows = mallowsProb(vote, sigma, phi)
            plackett = probPlackett(vote, pl_weights)
            delta_mallows += squaredDif(mallows, empirical)
            delta_plackett += squaredDif(plackett, empirical)
        else:
            empirical = 0
            mallows = mallowsProb(vote, sigma, phi)
            plackett = probPlackett(vote, pl_weights)
            delta_mallows += squaredDif(mallows, empirical)
            delta_plackett += squaredDif(plackett, empirical)
    
    table.append([num_votes, delta_mallows, delta_plackett])

# Pretty print results table

import pandas as pd

npdata = np.array(table)
results_df = pd.DataFrame(data=npdata,columns=col_names)
results_df.index += 1
pickle.dump(results_df, open('pickle/shortrun.p','wb'))

## Example of this shown directly after contents of this code
print(results_df)

# Examine information criterion now that we have goodness of fit

# Example data
mallows_debian = [122.55,178.23,2893.52,4990.13,207.46,476.65,197.95,101.64]
plackett_debian = [7.68,12.24,26.22,36.26,50.27,12.20,7.78,35.42]
num_alternatives = [4,5,7,8,9,5,4,8]

def AIC(likelihood, k):
    return (-2 * math.log(likelihood)) + (2*k)

for l in mallows_debian:
    aic = AIC(l, 2)
    print(l,"\t","%2.2f"%aic)

def BIC(likelihood, k, n):
    return k*math.log(n) - 2*math.log(likelihood)
    
for i in range(len(plackett_debian)):
    l = plackett_debian[i]
    k = num_alternatives[i]
    n = len(all_possible_votes(num_alternatives[i]))
    bic = BIC(l, k, n)
    print(l,'\t','%2.2f'%bic)