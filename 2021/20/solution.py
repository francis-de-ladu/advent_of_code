import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    ie_alg = np.asarray(list(puzzle[0]))
    ie_alg = np.where(ie_alg == '#', '1', '0')
    input_img = np.asarray([list(line) for line in puzzle[2:]])
    input_img = np.where(input_img == '#', '1', '0')
    return ie_alg, input_img


def part1(data, num_steps=2):
    ie_alg, grid = data
    out_char = '0'
    deltas = list(product(range(-1, 2), repeat=2))

    for step in range(num_steps):
        # new grid size is two more in each axis
        new_grid = np.zeros(np.asarray(grid.shape) + 2).astype(str)

        # ranges from -1 to shape-1, -1 will be mapped to last index of axis
        for pos in product(*map(lambda s: range(-1, s - 1), new_grid.shape)):
            binary = ''
            for x, y in map(lambda d: (pos[0] + d[0], pos[1] + d[1]), deltas):
                in_grid = (0 <= x < grid.shape[0]) and (0 <= y < grid.shape[1])
                binary += grid[x, y] if in_grid else out_char
            new_grid[pos] = ie_alg[int(binary, 2)]

        # roll by 1 in all axes to map indices -1 to shape-2 to 0 to shape-1
        grid = np.roll(new_grid, 1, axis=(0, 1))

        # update out of grid character
        out_char = ie_alg[0] if out_char == '0' else ie_alg[-1]

    return grid.astype(int).sum()


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_steps=50)

    # solutions to examples given for validation
    test_solutions = [
        (35, 3351),
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
