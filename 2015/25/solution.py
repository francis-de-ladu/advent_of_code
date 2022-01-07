import os
import re
import sys


def transform(puzzle):
    return [int(idx) for idx in re.findall(r'(\d+)', puzzle[0])]


def part1(data, first_code=20151125, mult=252533, mod=33554393):
    code_row, code_col = data
    code = first_code

    row = col = 1
    while row != code_row or col != code_col:
        if row > 1:
            row, col = row - 1, col + 1
        else:
            row, col = col + 1, 1

        code = (code * mult) % mod

    return code


def part2(data):
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
        (15514188, False),
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
