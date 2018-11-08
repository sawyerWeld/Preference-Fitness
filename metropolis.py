import random
import numpy as np
from tqdm import tqdm_notebook

def maximize(cost_model, lengths, params, gen_candidate, dataset, runs):
    initial_cost = cost_model(params, dataset, lengths)
    greatest_cost = initial_cost
    max_params = None
    
    for step in tqdm_notebook(range(runs), desc = cost_model.__name__):
        new_params = gen_candidate(params)
        prev_cost = cost_model(params, dataset, lengths)
        new_cost = cost_model(params, dataset, lengths)
        
        u = np.random.uniform(0,1)
        alpha = ((1.0 * new_cost) + 1)/ (prev_cost+1)

        if alpha > u:
            params = new_params
            prev_cost = new_cost
        
        if new_cost > greatest_cost:
            greatest_cost = new_cost
            max_params = params
        
    return max_params, greatest_cost