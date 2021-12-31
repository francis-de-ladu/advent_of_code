import os
import sys
from queue import Queue

import numpy as np

# <44016
#


def transform(puzzle):
    length = len(puzzle[0])
    return np.asarray([list(f'{line:{length}}') for line in puzzle])


def make_move(borrow, rooms):
    pass


def exit_room(borrow, rooms, room_idx):
    pass


def part1(data):
    print(data)
    costs = dict(zip("ABCD", 10**np.arange(4)))
    room_ids = [3, 5, 7, 9]
    return


def part2(data):
    new_data = np.asarray([list('  #D#C#B#A#  '), list('  #D#B#A#C#  ')])
    data = np.concatenate([data[:-2], new_data, data[-2:]], axis=0)
    print(data)
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
        # (12521, 44169),
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
