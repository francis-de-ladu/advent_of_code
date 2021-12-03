import os
import sys

import numpy as np


def transform(puzzle):
    trans_dict = dict(forward=(0, 1), down=(1, 1), up=(1, -1))
    move_tuples = [tuple(entry.split()) for entry in puzzle]
    return [(trans_dict.get(move), int(dist)) for move, dist in move_tuples]


def part1(instructions):
    position = np.asarray([0, 0])
    for ((axis, mult), dist) in instructions:
        position[axis] += mult * dist
    return np.prod(position)


def part2(instructions):
    position, aim = np.asarray([0, 0]), 0
    for ((axis, mult), dist) in instructions:
        if axis == 0:
            position += np.asarray([mult, aim]) * dist
        else:
            aim += mult * dist
    return np.prod(position)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    p1_solutions = [150]
    p2_solutions = [900]

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
