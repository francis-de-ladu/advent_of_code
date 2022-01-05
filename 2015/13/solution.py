import os
import sys
from itertools import permutations

import numpy as np


def transform(puzzle):
    entries = [line[:-1].replace('gain ', '+').replace('lose ', '-').split()
               for line in puzzle]
    entries = [(entry[0], int(entry[2]), entry[-1]) for entry in entries]

    attendees = set([entry[0] for entry in entries])
    attendees = {attendee: i for i, attendee in enumerate(sorted(attendees))}
    num_attendees = len(attendees)

    happiness = np.zeros([num_attendees, num_attendees])
    for att1, value, att2 in entries:
        happiness[attendees[att1], attendees[att2]] = value

    return happiness


def compute_best_happiness(data):
    data = data.astype(int)
    best_happiness = 0
    for order in permutations(range(data.shape[0])):
        total = data[order[0], order[-1]] + data[order[-1], order[0]]
        for i, j in zip(order, order[1:]):
            total += data[i, j] + data[j, i]
        best_happiness = max(total, best_happiness)

    return best_happiness


def part1(data):
    return compute_best_happiness(data)


def part2(data):
    data = np.concatenate([data, np.zeros([1, data.shape[1]])], axis=0)
    data = np.concatenate([data, np.zeros([data.shape[0], 1])], axis=1)
    return compute_best_happiness(data)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (330, None),
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
