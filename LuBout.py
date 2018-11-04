import logging
import numpy as np
import mallows_soi as mal


# Equation 2
def P(r, sigma, phi):
    return (phi ** (mal.ktdistanceSOI(r, sigma))) / Z(phi, len(r))

def test_Z():
    ans = Z(2, 3)
    print(ans)
    # 1             | 1
    # 1 + 2         | 3
    # 1 + 2 + 4     | 7
    # 1 + 2 + 4 + 8 | 15
    # 1 * 3 * 7 * 15 = 315
    assert(ans == 315)
    print('Test Passed')

# Equation 3
def Z(phi, m):
    product = 1
    for i in range(1, m):
        part = partial(phi, i)
        product *= part
    return product

def partial(phi, i):
    li = np.arange(i)
    seq = map(lambda x: phi ** x, li)
    return 1.0 * np.sum(np.fromiter(seq, dtype=np.int))

## Testing the probability function

data = mal.generateMallowsSet(5, 5, 0.8)
sigma = np.arange(5)
for rank in data:
    print(rank, P(rank, sigma, 0.5))