import os
import re
import sys

import numpy as np


def transform(puzzle):
    return puzzle


def get_slice(pos):
    return slice(pos[0], pos[1] + 1)


def part1(data):
    grid = np.zeros((1000, 1000)).astype(bool)
    for line in data:
        start, end = re.findall(r'\d+,\d+', line)
        start, end = map(int, start.split(',')), map(int, end.split(','))
        indexing = tuple(map(get_slice, zip(start, end)))
        if line.startswith('turn on'):
            grid[indexing] = True
        elif line.startswith('turn off'):
            grid[indexing] = False
        elif line.startswith('toggle'):
            grid[indexing] = ~grid[indexing]
        else:
            raise f'Invalid instruction `{line}`'

    return np.sum(grid)


def part2(data):
    grid = np.zeros((1000, 1000))
    for line in data:
        start, end = re.findall(r'\d+,\d+', line)
        start, end = map(int, start.split(',')), map(int, end.split(','))
        indexing = tuple(map(get_slice, zip(start, end)))
        if line.startswith('turn on'):
            grid[indexing] += 1
        elif line.startswith('turn off'):
            grid[indexing] = np.maximum(0, grid[indexing] - 1)
        elif line.startswith('toggle'):
            grid[indexing] += 2
        else:
            raise f'Invalid instruction `{line}`'

    return np.sum(grid).astype(int)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (None, False),
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
