import os
import sys

import numpy as np


def transform(puzzle):
    return list(map(int, puzzle))


def part1(measures):
    measures = np.asarray(measures)
    return np.sum((measures[1:] > measures[:-1]).astype(int))


def part2(measures, window_size=3):
    tuples = zip(*[measures[offset:] for offset in range(window_size)])
    summed = list(map(sum, tuples))
    return part1(summed)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    p1_solutions = [7]
    p2_solutions = [5]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        p1_solutions=p1_solutions,
        p2_solutions=p2_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
