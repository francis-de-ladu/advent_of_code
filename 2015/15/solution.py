import os
import re
import sys
from itertools import combinations_with_replacement

import numpy as np


def transform(puzzle):
    pattern = re.compile(r'[:,]?\s')
    entries = [re.split(pattern, line)[2::2] for line in puzzle]
    entries = [list(map(int, props)) for props in entries]
    return np.asarray(entries, dtype=int)


def part1(data, num_spoons=100, num_calories=None):
    rng, cnt = range(num_spoons + 1), data.shape[0] - 1

    best_score = 0
    for indices in combinations_with_replacement(rng, cnt):
        indices = (0,) + indices + (100,)
        tsps = [nxt - cur for cur, nxt in zip(indices, indices[1:])]
        tsps = np.asarray(tsps).reshape([data.shape[0], 1])
        score = np.clip(np.sum(tsps * data, axis=0), 0, None)
        if num_calories is None or score[-1] == num_calories:
            best_score = max(score[:-1].prod(), best_score)

    return best_score


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_calories=500)

    # solutions to examples given for validation
    test_solutions = [
        (62842880, 57600000),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
