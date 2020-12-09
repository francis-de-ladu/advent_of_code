from itertools import combinations

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

puzzle = list(map(int, puzzle))


# part 1

PREAMBLE_LEN = 25

for i in range(PREAMBLE_LEN, len(puzzle)):
    to_consider = puzzle[i - PREAMBLE_LEN:i]
    if puzzle[i] not in set([a + b for a, b in combinations(to_consider, 2)]):
        invalid = puzzle[i]
        break

print(invalid)


# part 2

for i in range(len(puzzle)):
    for j in range(i, len(puzzle)):
        current_sum = sum(puzzle[i:j + 1])
        if current_sum >= invalid:
            break
    if current_sum == invalid:
        break

print(min(puzzle[i:j + 1]) + max(puzzle[i:j + 1]))
