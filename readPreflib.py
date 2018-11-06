# Reading in data from the preflib format

from random import shuffle
from collections import defaultdict


def readinSOIdata(filename):

    candidates = {}

    votes = []

    with open(filename) as file:
        data = file.readlines()
        num_alternatives = int(data[0])

        # Make Candidate Names Dict
        for i in range(1, num_alternatives+1):
            string = data[i]
            split_pos = string.find(',') + 1
            candidates[i] = string[split_pos:-2]

        # Wrangel Orderings
        for i in range(num_alternatives+2, len(data)):
            row = data[i].split(',')
            num_occurances = int(row[0])
            nums = list(map(int, row[1:]))

            if len(nums) == num_alternatives:
                for _ in range(num_occurances):
                    votes.append(nums)
            else:
                # Randomly add unused alternatives
                pos = list(range(1,num_alternatives+1))
                for num in nums:
                    pos.remove(num)
                for _ in range(num_occurances):
                    shuffle(pos)
                    votes.append(nums + pos)

    return candidates, votes

def readinSOIwfreqs(filename):

    candidates = {}

    votes = []

    with open(filename) as file:
        data = file.readlines()
        num_alternatives = int(data[0])

        # Make Candidate Names Dict
        for i in range(1, num_alternatives+1):
            string = data[i]
            split_pos = string.find(',') + 1
            candidates[i] = string[split_pos:-2]

        # Wrangel Orderings
        for i in range(num_alternatives+2, len(data)):
            row = data[i].split(',')
            num_occurances = int(row[0])
            nums = list(map(int, row[1:]))
            votes.append((num_occurances, nums))


    return candidates, votes


def soiInputwithWeights(filename):

    candidates = {}

    votes = []

    length_counts = defaultdict(int)

    with open(filename) as file:
        data = file.readlines()
        num_alternatives = int(data[0])

        # Make Candidate Names Dict
        for i in range(1, num_alternatives+1):
            string = data[i]
            split_pos = string.find(',') + 1
            candidates[i] = string[split_pos:-2]

        # Wrangel Orderings
        for i in range(num_alternatives+2, len(data)):
            row = data[i].split(',')
            num_occurances = int(row[0])
            nums = list(map(int, row[1:]))
            length_counts[len(nums)] += num_occurances
            votes.append((num_occurances, nums))


    return candidates, length_counts, votes
