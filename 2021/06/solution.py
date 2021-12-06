import os
import sys
from collections import defaultdict


def transform(puzzle):
    fishes = defaultdict(int)
    for timer in map(int, puzzle[0].split(',')):
        fishes[timer] += 1
    return fishes


def part1(data, num_days=80):
    spawn_rate = 7
    first_cycle_delay = 2

    for _ in range(num_days):
        new_data = defaultdict(int)
        for key in data:
            new_key = key - 1
            if new_key < 0:
                new_key += spawn_rate
                new_data[new_key + first_cycle_delay] += data[key]
            new_data[new_key] += data[key]

        data = new_data

    return sum(data.values())


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict(num_days=80)
    p2_kwargs = dict(num_days=256)

    # solutions to examples given for validation
    test_solutions = [
        (5934, 26984457539),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
