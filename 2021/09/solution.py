import math
import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    return np.stack([list(map(int, line)) for line in puzzle], axis=0)


def get_neighbors(coords, dims):
    neighbors = []
    for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        x, y = coords[0] + dx, coords[1] + dy
        if 0 <= x < dims[0] and 0 <= y < dims[1]:
            neighbors.append((x, y))
    return neighbors


def get_lowest_locations(data):
    lowest_locations = []
    for coords in product(*map(range, data.shape)):
        neighbors = get_neighbors(coords, data.shape)
        if data[coords] < np.min(data[list(zip(*neighbors))]):
            lowest_locations.append(coords)
    return lowest_locations


def explore(data, coords, seen=None):
    seen = set() if seen is None else seen
    if coords in seen or data[coords] == 9:
        return seen

    seen.add(coords)

    for neighbor in get_neighbors(coords, data.shape):
        explore(data, neighbor, seen)

    return seen


def part1(data):
    lowest_locations = get_lowest_locations(data)
    lowest_points = data[list(zip(*lowest_locations))]
    return np.sum(lowest_points) + len(lowest_points)


def part2(data, num_largest=3):
    lowest_locations = get_lowest_locations(data)

    basins = []
    for coords in lowest_locations:
        basin = explore(data, coords)
        basins.append(basin)

    largest_basins = sorted(basins, key=len, reverse=True)
    return math.prod(map(len, largest_basins[:num_largest]))


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
