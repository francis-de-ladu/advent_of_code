import os
import sys

import numpy as np


def transform(puzzle):
    return puzzle


def part1(data, forbidden={'ab', 'cd', 'pq', 'xy'}):
    nice_string_cnt = 0
    for string in data:
        num_voyels = sum(string.count(v) for v in 'aeiou')
        has_double = any(c1 == c2 for c1, c2 in zip(string, string[1:]))
        is_forbidden = any(f in string for f in forbidden)
        if num_voyels >= 3 and has_double and not is_forbidden:
            nice_string_cnt += 1

    return nice_string_cnt


def part2(data):
    nice_string_cnt = 0
    for string in data:
        has_repeated_pair = False
        for i in range(len(string)):
            if string[i:i + 2] in string[i + 2:]:
                has_repeated_pair = True
                break
        has_spaced_repeat = any(c1 == c2 for c1, c2 in zip(string, string[2:]))
        if has_repeated_pair and has_spaced_repeat:
            nice_string_cnt += 1

    return nice_string_cnt


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (1, None),
        (1, None),
        (0, None),
        (0, None),
        (0, None),
        (None, 1),
        (None, 1),
        (None, 0),
        (None, 0),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
