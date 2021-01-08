# Converted from IPython Notebook to .py file for inclusion in thesis
# In this code the central ranking is referred to as sigma

def mallowsProb(r, sigma, phi):
    return (1.0 / Z(phi, len(r)-1) * math.exp(-1.0 * phi * kt(r, sigma)))

# Normalization Term Z
def Z(phi, m):
    product = 1
    for i in range(1, m):
        part = 0
        for j in range(0,i):
            part += math.exp(-1 * (phi ** j))
        product *= part
    return product   

# Kendall-Tau Distance
def kt(a, b):
    unique_set =  np.unique(np.concatenate([a,b]))
    pairs = itertools.combinations(unique_set, 2)
    count = 0.0
    for i, j in pairs:
        unknown = False
        try:
            first = np_index(a, i) - np_index(a, j)
            secnd = np_index(b, i) - np_index(b, j)
        except:
            unknown = True
            count += 0.5
        if not unknown and (first * secnd < 0):
            count += 1
    return count

def mallowsCost(params, dataset, lengths):
    central_ranking, phi = params
    cost = 0
    for tup in dataset:
        num_occurances, r = tup
        cost += num_occurances * mallowsProb(r, central_ranking, phi)
    return cost 

def generateMallowsCandidate(params):
    sigma, phi = params
    new_sigma = generateSigma(sigma)
    new_phi = generatePhi(phi)
    return [new_sigma, new_phi]

def generateSigma(order):
    tuning_parameter = 0.25
    a = np.random.randint(len(order))
    b = np.random.randint(len(order))
    order[a], order[b] = order[b], order[a]
    while (np.random.uniform(0.0, 1.0) >= tuning_parameter):
        a = np.random.randint(len(order))
        b = np.random.randint(len(order))
        order[a], order[b] = order[b], order[a]
    return order

def generatePhi(phi):
    alpha = 0.3 # tuning param
    delta = np.random.uniform(-1 * alpha,alpha)
    new = phi + delta
    while(new <= 0):
        delta = np.random.uniform(-1 * alpha,alpha)
        new = phi + delta
    return new   

def runMallows(rankings, num_alternatives, n_runs, lengths_vector):
    lengths = getLengthProbs(lengths_vector)
    if complete:
        num_alternatives = list(lengths_vector.keys())[0]
    initial_sigma = np.arange(num_alternatives) + 1
    initial_params = [initial_sigma, 1.0]
    costfunc = mallowsCost
    if complete:
        costfunc = mallowsCostComplete
    params, cost = metropolis.maximize(costfunc, lengths, initial_params, generateMallowsCandidate, rankings, n_runs)
    sigma, phi = params
    return params

def save():
    import pickle
    pickle.dump(params, open('pickle/mallowsoutput.p','wb'))