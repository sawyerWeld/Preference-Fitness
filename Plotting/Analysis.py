# Analysis of the output of the markov process used to estimate parameters of preference datasets

import matplotlib.pyplot as plt

# Heres how this should work
# Take in the outputs of the metropolis algorithm, list of lists and associated nums
# Now we are only looking at the lists, we don't care about the numbers here because
# we have R code for that

# We make a dict of lists and the number of occurences of that preference

occurances = {}
costs = {}

def makeFrequencyTable(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        for line in data:
            parts = line.split()
            li = []
            cost = int(parts[1])
            for char in parts[0]:
                li.append(int(char))
            ordering = tuple(li)
            if ordering in occurances:
                num = occurances[ordering]
                occurances[ordering] = num + 1
            else:
                occurances[ordering] = 1
                costs[ordering] = cost

makeFrequencyTable('/data_output/mallows_data.txt')

costOccurances = []

def makeCostVsOccurances():
    for ordering, freq in occurances.items():
        cost = costs[ordering]
        costOccurances.append((cost, freq))

makeCostVsOccurances()

x, y = zip(*costOccurances)
plt.scatter(x,y)
# plt.title('Mallow\'s Distribution. N=1M Burnout=50k')
plt.xlabel('Cost Function')
plt.ylabel('Frequency')
plt.show()