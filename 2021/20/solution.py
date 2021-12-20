import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    ie_alg = np.asarray(list(puzzle[0]))
    input_img = np.asarray([list(line) for line in puzzle[2:]])
    return ie_alg, input_img


def part1(data, num_steps=2):
    ie_alg, grid = data
    is_flashing = ie_alg[0] == '#' and ie_alg[1] == '.'

    for step in range(num_steps):
        # new grid size is two more in each axis
        new_grid = np.zeros(np.asarray(grid.shape) + 2).astype(str)

        for x_new, y_new in product(*map(range, new_grid.shape)):
            # shift coords in new grid to get associated coords in old grid
            x_old, y_old = x_new - 1, y_new - 1

            binary = ''
            for dx, dy in product(range(-1, 2), repeat=2):
                # compute pos with deltas
                pos_x, pos_y = x_old + dx, y_old + dy

                # if pos is within limits, get value from grid,
                # else compute value from idx 0 and 511 of the algorithm
                if 0 <= pos_x < grid.shape[0] and 0 <= pos_y < grid.shape[1]:
                    binary += '1' if grid[pos_x, pos_y] == '#' else '0'
                elif ie_alg[0] == '#':
                    if is_flashing:
                        binary += '0' if step % 2 == 0 else '1'
                    else:
                        binary += '1'
                else:
                    binary += '0'

            # add value to new grid
            new_grid[x_new, y_new] = ie_alg[int(binary, 2)]

        # new grid becomes the current grid
        grid = new_grid

    return np.sum(grid == '#')


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
