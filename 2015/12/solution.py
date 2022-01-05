import json
import os
import sys
from functools import partial


def transform(puzzle):
    return json.loads(puzzle[0])


def sum_numbers(data, excluded_prop):
    sum_func = partial(sum_numbers, excluded_prop=excluded_prop)
    if isinstance(data, str):
        return 0
    elif isinstance(data, int):
        return data
    elif isinstance(data, list):
        return sum(map(sum_func, data))
    elif isinstance(data, object):
        if excluded_prop in data.keys() or excluded_prop in data.values():
            return 0
        sum_keys = sum(map(sum_func, data.keys()))
        sum_values = sum(map(sum_func, data.values()))
        return sum_keys + sum_values

    print(f'Invalid data type `{type(data)}`')
    exit()


def part1(data, excluded_prop=None):
    return sum_numbers(data, excluded_prop)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(excluded_prop='red')

    # solutions to examples given for validation
    test_solutions = [
        (6, 6),
        (6, 6),
        (3, 3),
        (3, 3),
        (0, 0),
        (0, 0),
        (0, 0),
        (0, 0),
        (None, 4),
        (None, 0),
        (None, 6),
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
