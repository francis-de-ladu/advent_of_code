import os
import sys

import numpy as np


def transform(puzzle):
    entries = [line.split() for line in puzzle]
    entries = [tuple(int(entry[i]) for i in (3, 6, 13)) for entry in entries]
    return entries


def part1(data, num_seconds=2503):
    dists = []
    for speed, duration, rest in data:
        dist, elapsed = 0, 0
        while elapsed < num_seconds:
            duration = min(duration, num_seconds - elapsed)
            dist += speed * duration
            elapsed += duration + rest
        dists.append(dist)

    return max(dists)


def part2(data, num_seconds=2503):
    dists = np.zeros([len(data), num_seconds], dtype=int)
    for i, (speed, duration, rest) in enumerate(data):
        dist, elapsed = 0, 0
        while elapsed < num_seconds:
            duration = min(duration, num_seconds - elapsed)
            traveled = speed * (np.arange(duration) + 1)
            dists[i, elapsed:elapsed + duration] = dist + traveled
            dist += speed * duration
            elapsed += duration

            rest = min(rest, num_seconds - elapsed)
            dists[i, elapsed:elapsed + rest] = dist
            elapsed += rest

    points = np.sum(dists == dists.max(axis=0), axis=1)
    return points.max()


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        # (1120, 689),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
