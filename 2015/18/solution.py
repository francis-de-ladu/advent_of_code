import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    grid = np.asarray([list(line) for line in puzzle])
    grid = np.where(grid == '#', 1, 0)
    return grid


def get_square_slice(pos, radius=1):
    return map(lambda c: slice(max(0, c - radius), c + radius + 1), pos)


def part1(grid, num_steps=100):
    for step in range(num_steps):
        new_grid = np.empty_like(grid)
        for pos in product(*map(range, grid.shape)):
            indexing = tuple(get_square_slice(pos))
            num_lit = np.sum(grid[indexing]) - grid[pos]
            new_grid[pos] = int(num_lit == 3 or grid[pos] and num_lit == 2)
        grid = new_grid

    return grid.sum()


def part2(grid, num_steps=100):
    h, w = grid.shape
    corners = set([(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)])
    grid[tuple(zip(*corners))] = 1

    for step in range(num_steps):
        new_grid = np.empty_like(grid)
        for pos in product(*map(range, grid.shape)):
            if pos in corners:
                new_grid[pos] = 1
                continue
            indexing = tuple(get_square_slice(pos))
            num_lit = np.sum(grid[indexing]) - grid[pos]
            new_grid[pos] = int(num_lit == 3 or grid[pos] and num_lit == 2)
        grid = new_grid

    return grid.sum()


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        # (4, 17),
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
