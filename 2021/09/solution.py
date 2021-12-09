import math
import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    return np.stack([list(map(int, line)) for line in puzzle], axis=0)


def get_lowest_locations(data):
    lowest_locations = []
    for ii, jj in product(*map(range, data.shape)):
        i, iii = max(0, ii - 1), ii + 1
        j, jjj = max(0, jj - 1), jj + 1
        if np.amin(data[i:iii + 1, j:jjj + 1]) == data[ii, jj]:
            lowest_locations.append((ii, jj))
    return lowest_locations


def explore(data, coords, seen=None):
    seen = set() if seen is None else seen
    if coords in seen or data[coords] == 9:
        return seen

    seen.add(coords)

    x, y = coords
    if x > 0:
        explore(data, (x - 1, y), seen)
    if y > 0:
        explore(data, (x, y - 1), seen)
    if x < data.shape[0] - 1:
        explore(data, (x + 1, y), seen)
    if y < data.shape[1] - 1:
        explore(data, (x, y + 1), seen)


def part1(data):
    lowest_locations = get_lowest_locations(data)
    lowest_points = data[list(zip(*lowest_locations))]
    return np.sum(lowest_points) + len(lowest_points)


def part2(data):
    lowest_locations = get_lowest_locations(data)

    basins = []
    for coords in lowest_locations:
        basins.append(explore(data, coords))

    num_largest = 3
    largest_basins = sorted(basins, key=len, reverse=True)[:num_largest]
    return math.prod(map(len, largest_basins))


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (15, 1134),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
