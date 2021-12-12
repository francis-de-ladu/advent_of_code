import os
import sys

import numpy as np


def transform(puzzle):
    return puzzle[0]


def part1(data, func=len):
    x, y = 0, 0
    visited = {(x, y)}

    for c in data:
        if c == '<':
            x -= 1
        elif c == '>':
            x += 1
        elif c == '^':
            y -= 1
        elif c == 'v':
            y += 1
        visited.add((x, y))

    return func(visited)


def part2(data):
    def func(x): return x
    santa = part1(data[::2], func)
    robo = part1(data[1::2], func)
    return len(santa.union(robo))


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (4, 3),
        (2, 11),
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
