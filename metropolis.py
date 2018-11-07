import random
import numpy as np
from tqdm import tqdm_notebook

def maximize(cost_model, params, gen_candidate, dataset, runs):
    initial_cost = cost_model(params, dataset)
    greatest_cost = initial_cost
    max_params = None
    
    for step in tqdm_notebook(range(runs)):
        new_params = gen_candidate(params)
        prev_cost = cost_model(params, dataset)
        new_cost = cost_model(params, dataset)
        
        u = np.random.uniform(0,1)
        alpha = (1.0 * new_cost) / prev_cost

        if alpha > u:
            params = new_params
            prev_cost = new_cost
        
        if new_cost > greatest_cost:
            greatest_cost = new_cost
            max_params = params
        
    return max_params, greatest_cost