import math
import os
import sys
from itertools import combinations

import numpy as np


def transform(puzzle):
    return sorted([int(weight) for weight in puzzle], reverse=True)


def part1(packages, containers=[[], []]):
    target_weight = sum(packages) // (len(containers) + 1)
    weights = np.zeros([len(packages) + 1, target_weight + 1], dtype=int)
    sizes = np.zeros_like(weights)

    # knapsack problem
    for i, pack in enumerate(packages):
        for w in np.arange(target_weight) + 1:
            if pack > w or weights[i, w] >= weights[i, w - pack] + pack:
                weights[i + 1, w] = weights[i, w]
                sizes[i + 1, w] = sizes[i, w]
            else:
                weights[i + 1, w] = weights[i, w - pack] + pack
                sizes[i + 1, w] = sizes[i, w - pack] + 1

    # retrieve minimum size of configurations where target weight is reached
    min_size = int(np.min(np.where(weights == target_weight, sizes, np.inf)))
    del weights, sizes

    # retrieve minimum quantum entanglement of valid configs with minimum size
    min_qe = float('inf')
    for packs in combinations(packages, r=int(min_size)):
        if sum(packs) == target_weight:
            qe = math.prod(packs)
            if qe < min_qe:
                min_qe = qe
                passenger_seat = packs

    # check if possible to split remaining packages equally between containers
    remaining = [pack for pack in packages if pack not in passenger_seat]
    if has_possible_split(remaining, containers, target_weight):
        return min_qe

    return None


def has_possible_split(packages, containers, target_weight):
    if len(packages) == 0:
        return True

    for i, _ in enumerate(packages):
        current, others = packages[i], packages[:i] + packages[i + 1:]
        for j, container in enumerate(containers):
            expected_weight = sum(container) + current
            if expected_weight <= target_weight:
                new_container = container + [current]
                new_containers = \
                    containers[:j] + [new_container] + containers[j + 1:]

                if has_possible_split(others, new_containers, target_weight):
                    return True
    else:
        return False


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(containers=[[], [], []])

    # solutions to examples given for validation
    test_solutions = [
        (99, 44),
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
