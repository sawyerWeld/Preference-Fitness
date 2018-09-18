# functions for estimating parameters of plackett-luce distributions
import mallows
import numpy as np

weights_defined = False
weights = -1

def genCandidate(tup):
    return mallows.genCandidate(tup)


# Here is where I need to calculate prior values
# Not super sure how to do this
# Been reading Hinderson, Kirrane (2018)

# Here is my attempted method:
# Sum the ranking that each alternative received in each ordering
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
    inverted = np.zeros(N)
    for i in range(len(sums)):
        inverted[i] = 1.0 / sums[i]
    global weights
    weights = normalize(inverted)


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

    ordering = list(params)
    product = 1
    for i in range(len(ordering)-1):
        num = weights[i]
        denom = 0
        for j in range(i+1, len(ordering)):
            denom += weights[j]
        product *= (num/denom)
    return 1.0 / product

data = [np.arange(5), np.arange(5)]
defineWeights(data)
print(weights)



