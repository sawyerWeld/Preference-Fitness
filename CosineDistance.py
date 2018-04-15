# Expirementing with Cosine Distance of Preferences

import numpy as np
from itertools import permutations
import mallows


def cosDistance(a, b):
    if len(a) != len(b):
        print("wrong lengths")
    l = len(a)
    # denom = (l * (l + 1)) / 2
    denom = 0
    for i in a:
        denom += i ** 2
    numer = np.dot(a, b)
    return 1 - (numer / denom)

a = np.arange(7)

perm = list(permutations(a))
print(len(perm))

# for p in perm:
#     print(mallows.ktdistance(a, p), cosDistance(a, p))


f = open("cosine_vs_ktau.txt", mode='w')
for p in perm:
    mal = mallows.ktdistance(a, p)
    cos = cosDistance(a, p)
    f.write('%s %s\n' % (str(mal), str(cos)))
f.close()
