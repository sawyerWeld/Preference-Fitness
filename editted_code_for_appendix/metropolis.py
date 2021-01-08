# Metropolis.py

import random
import numpy as np
from collections import deque
from tqdm import tqdm_notebook

def maximize(cost_model, lengths, params, gen_candidate, dataset, runs, consec=15):
    initial_cost = cost_model(params, dataset, lengths)
    greatest_cost = initial_cost
    max_params = params
    
    previous_n = deque(np.arange(consec), consec)

    for step in tqdm_notebook(range(runs), desc = cost_model.__name__):
        new_params = gen_candidate(params)
        prev_cost = cost_model(params, dataset, lengths)
        new_cost = cost_model(new_params, dataset, lengths)
        
        u = np.random.uniform(0,1)
        alpha = ((1.0 * new_cost) )/ (prev_cost)
        # print(u, alpha)

        if alpha > u:
            params = new_params
            prev_cost = new_cost
            # print(params, cost_model.__name__)

        
        if new_cost > greatest_cost:
            greatest_cost = new_cost
            max_params = params
        
        previous_n.appendleft(prev_cost)
        if previous_n.count(previous_n[0]) == len(previous_n):
            print('stopped after ', step)
            break

    print(previous_n)
    return max_params, greatest_cost
    