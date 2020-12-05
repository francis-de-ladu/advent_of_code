import operator
from functools import reduce
from itertools import combinations

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

input_values = sorted(map(int, puzzle))


# puzzle 1

for vals in combinations(input_values, 2):
    if sum(vals) == 2020:
        break

print(reduce(operator.mul, vals))


# puzzle 2

for vals in combinations(input_values, 3):
    if sum(vals) == 2020:
        break

print(reduce(operator.mul, vals))
