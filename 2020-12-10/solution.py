import re

import numpy as np

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

puzzle = [0] + sorted(map(int, puzzle))
puzzle.append(puzzle[-1] + 3)

puzzle = np.asarray(puzzle)


# part 1

diffs = puzzle[1:] - puzzle[:-1]
unique, counts = np.unique(diffs, return_counts=True)
diff_counts = dict(zip(unique, counts))

print(diff_counts[1] * diff_counts[3])


# part 2

diffs_str = ''.join(map(str, diffs.tolist()))
diffs = re.split(r"(?:3+)", diffs_str)  # split the string on 3s

arrangments = 1
for group in diffs:
    arrangments *= sum(range(1, len(group))) + 1
