import os
import sys
from heapq import heappop, heappush

import numpy as np


def transform(puzzle):
    return np.asarray([list(map(int, line)) for line in puzzle])


def get_risk_at(risk_map, pos):
    h, w = risk_map.shape
    x_pos, x_tile = pos[0] % h, pos[0] // h
    y_pos, y_tile = pos[1] % w, pos[1] // w
    return (risk_map[x_pos, y_pos] + x_tile + y_tile - 1) % 9 + 1


def get_neighbors(pos, pos_risk, risk_map, max_x, max_y):
    neighbors = []
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        x, y = pos[0] - dx, pos[1] - dy
        if 0 <= x < max_x and 0 <= y < max_y:
            neighbors.append((x, y))

    risks = [pos_risk + get_risk_at(risk_map, neigh) for neigh in neighbors]
    return neighbors, risks


def part1(risk_map, num_repeats=1):
    h, w = np.asarray(risk_map.shape) * num_repeats
    START, END = (0, 0), (h - 1, w - 1)

    total_risk = {START: 0}
    heap = [(total_risk[START], START)]

    while END not in total_risk:
        min_risk, min_pos = heappop(heap)
        neighbors, risks = get_neighbors(min_pos, min_risk, risk_map, h, w)

        for neigh, risk in zip(neighbors, risks):
            if risk < total_risk.get(neigh, np.inf):
                total_risk[neigh] = risk
                heappush(heap, (risk, neigh))

    return int(total_risk[END])


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_repeats=5)

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
