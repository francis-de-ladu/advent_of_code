import os
import sys
from heapq import heappop, heappush

import numpy as np


def transform(puzzle):
    return np.asarray([list(map(int, line)) for line in puzzle])


def get_tile(risk_map, i):
    return np.where(risk_map + i < 10, risk_map + i, (risk_map + i) % 10 + 1)


def get_neighbors(pos, pos_risk, risk_map):
    x, y = pos
    neighbors = []
    for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= xx < risk_map.shape[0] and 0 <= yy < risk_map.shape[1]:
            neighbors.append((xx, yy))

    risks = [pos_risk + risk_map[neigh] for neigh in neighbors]
    return neighbors, risks


def part1(risk_map, num_repeat=1):
    risk_map = np.concatenate(
        [get_tile(risk_map, i) for i in range(num_repeat)], axis=0)
    risk_map = np.concatenate(
        [get_tile(risk_map, i) for i in range(num_repeat)], axis=1)

    total_risk = np.ones_like(risk_map) * np.inf
    total_risk[0, 0] = 0

    heap = [(0, (0, 0))]

    while total_risk[-1, -1] == np.inf:
        min_risk, min_pos = heappop(heap)
        neighbors, risks = get_neighbors(min_pos, min_risk, risk_map)
        for neigh, risk in zip(neighbors, risks):
            if risk < total_risk[neigh]:
                total_risk[neigh] = risk
                heappush(heap, (risk, neigh))

    return int(total_risk[-1, -1])


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_repeat=5)

    # solutions to examples given for validation
    test_solutions = [
        (40, 315),
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
