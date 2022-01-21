import os
import sys

import numpy as np


def transform(puzzle):
    seafloor = np.stack([list(line) for line in puzzle])
    return seafloor


def part1(seafloor):
    cucumbers = [('>', 1), ('v', 0)]

    num_steps = 0
    new_seafloor = None
    while np.any(seafloor != new_seafloor):
        if new_seafloor is not None:
            seafloor = new_seafloor

        num_steps += 1
        new_seafloor = seafloor.copy()
        for kind, axis in cucumbers:
            dest_is_empty = np.roll(new_seafloor, -1, axis=axis) == '.'
            can_move = (new_seafloor == kind) & dest_is_empty

            new_seafloor = np.where(can_move, '.', np.where(
                np.roll(can_move, 1, axis=axis), kind, new_seafloor))

    return num_steps


def part2(seafloor):
    return


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (58, False),
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
