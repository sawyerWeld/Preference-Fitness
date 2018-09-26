# functions for estimating parameters of plackett-luce distributions
import mallows
import numpy as np
import itertools
import tqdm 

weights_defined = False
weights = -1

def genCandidate(tup):
    return [mallows.generateOrdering(tup[0])]


# Here is where I need to calculate prior values
# Not super sure how to do this
# Been reading Hinderson, Kirrane (2018)

# Here is my attempted method:
# Sum the rank that each alternative received in each ordering
# let D_i = the ith ordering in our dataset
# let α_ni = the ranking alternative n in D_i
# sums[n] = [ sum{i=0,i=|D|}(α_ni) for all i ]
# let inverted = (1 / sums)
# weights = L2 norm of inverted
def defineWeights(dataset):
    N = len(dataset[0])
    sums = np.zeros(N)
    for ranking in dataset:
        for i in range(len(ranking)):
            place = ranking[i]
            sums[place] += i + 1
    sums = normalize(sums)
    global weights
    weights = sums


def normalize(vector):
    scale = 1.0 / np.sum(vector)
    return vector * scale

# let N = |ordering|
# let λ(a) = the weight assigned to ordering[a]
# p(ordering) = product{i=0,i=N-1}(λ(i)/sum{j=i,j=N}(λ(j)))

def costFunction(params, data):
    global weights_defined
    if not weights_defined:
        defineWeights(data)
        weights_defined = True
        
    ordering = list(params[0])
    return costFunctionHelper(ordering, data)

def costFunctionHelper(ordering, data):
    product = 1.0
    # print(ordering)
    for i in range(len(ordering)-1):
        num = weights[ordering[i]]
        denom = 0.0
        # print(num, i,  ordering[i], 'hello')
        for j in range(i+1, len(ordering)):
            denom += weights[ordering[j]]
        product *= (num/denom)
        # print(num, denom)
    return 1.0 / product

def pl_curve_test():
    orderings = mallows.generateMallowsSet(10, 3, 0.8, centroid=[2,1,0])
    defineWeights(orderings)
    print('weights', weights)
    ranking = list(range(3))
    for perm in itertools.permutations(ranking):
        print(perm, costFunctionHelper(perm, ranking), '\n\n')
    print('done')

# pl_curve_test()
