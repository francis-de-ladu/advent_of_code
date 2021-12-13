import os
import re
import sys
import time


def transform(puzzle):
    assert part1('1', num_iters=5, to_result=lambda x: x) == '312211'
    return puzzle[0]


def read_aloud(group):
    return f'{len(group)}{group[0]}'


def part1(data, num_iters=40, to_result=len):
    pattern = re.compile(r'(?<=([\d\s]))([^\1])\2*')
    for _ in range(num_iters):
        groups = [x.group() for x in re.finditer(pattern, f' {data}')]
        data = ''.join(map(read_aloud, groups))

    return to_result(data)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_iters=50)

    # solutions to examples given for validation
    test_solutions = [
        (None, None),
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
