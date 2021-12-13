import json
import os
import sys


def transform(puzzle):
    return puzzle


def part1(data, func):
    code_chars, mem_chars = 0, 0
    for line in map(func, data):
        code_chars += len(line) + 2
        mem_chars += len(line.encode().decode('unicode_escape'))

    return code_chars - mem_chars


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict(func=lambda x: x)
    p2_kwargs = dict(func=json.dumps)

    # solutions to examples given for validation
    test_solutions = [
        (12, 19),
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
