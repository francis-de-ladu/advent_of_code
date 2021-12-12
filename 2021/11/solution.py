import os
import sys

import numpy as np


def transform(puzzle):
    octopuses = [[int(oct) for oct in line] for line in puzzle]
    return np.asarray(octopuses)


def get_square_slice(pos):
    return map(lambda p: slice(max(0, p - 1), p + 2), pos)


def part1(octopuses, full_flash=False):
    flash_cnt = 0
    num_steps = int(1e10) if full_flash else 100

    for step in range(1, num_steps + 1):
        flashed = np.zeros_like(octopuses)
        octopuses += 1

        to_flash = np.argwhere((octopuses > 9) & ~flashed)

        while to_flash.size:
            for square in map(get_square_slice, to_flash):
                octopuses[tuple(square)] += 1

            flashed[tuple(zip(*to_flash))] = 1
            to_flash = np.argwhere((octopuses > 9) & ~flashed)

        octopuses = np.where(octopuses > 9, 0, octopuses)
        flash_cnt += np.sum(flashed)

        if full_flash and np.all(flashed):
            return step + 1

    return flash_cnt


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(full_flash=True)

    # solutions to examples given for validation
    test_solutions = [
        (1656, 195),
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
