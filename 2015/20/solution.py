import math
import os
import sys

import numpy as np


def transform(puzzle):
    return int(puzzle[0])


def is_divisible_by(house, value):
    return house % value == 0


def part1(num_presents):
    house_1 = house_2 = None

    house = 0
    while not (house_1 and house_2):
        house += 1
        if not all([is_divisible_by(house, value) for value in (3, 5, 7, 8)]):
            continue

        presents_1 = presents_2 = 0
        for elf in range(1, house + 1):
            if house % elf == 0:
                presents_1 += elf
                if house <= 50 * elf:
                    presents_2 += elf

        if not house_1 and 10 * presents_1 >= num_presents:
            house_1 = house
        if not house_2 and 11 * presents_2 >= num_presents:
            house_2 = house

    return house_1, house_2


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (False, False),
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
