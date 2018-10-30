import numpy as np
import matplotlib.pyplot as plt

def count_swaps(N, eta):
    c = 0
    for i in range(1, N):
        for j in range(i, 0, -1):
            if eta >= np.random.uniform(0.0,1.0):
                c += 1
    return c

# print(count_swaps(10, 0.5))

def analysis(num_iters, N_min, N_max, N_inc, eta):
    out = []
    for N in range(N_min, N_max+1, N_inc):
        this_N = []
        for _ in range(num_iters):
            this_N.append(count_swaps(N, eta) * 1.0)
        out.append((N, np.sum(this_N) / num_iters))
    return out

print(analysis(10, 0, 100, 1,  0.5))

x, y = zip(*analysis(10, 0, 100, 1,  0.5))
plt.scatter(x,y)
# plt.title('Mallow\'s Distribution. N=1M Burnout=50k')
plt.xlabel('Cost Function')
plt.ylabel('Frequency')
plt.show()