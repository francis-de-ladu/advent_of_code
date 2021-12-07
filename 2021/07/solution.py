import os
import sys

import numpy as np


def transform(puzzle):
    return np.asarray(list(map(int, puzzle[0].split(','))))


def compute_fuel(data, mean):
    dist = np.abs(data - mean).astype(int)
    return np.sum(dist * (dist + 1) // 2)


def part1(data):
    median = np.median(data)
    return np.sum(np.abs(data - median)).astype(int)


def part2(data):
    mean = np.mean(data)
    fuel_floor = compute_fuel(data, np.floor(mean))
    fuel_ceil = compute_fuel(data, np.ceil(mean))
    return fuel_floor if fuel_floor < fuel_ceil else fuel_ceil


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (37, 168),
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
