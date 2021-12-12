import hashlib
import os
import sys


def transform(puzzle):
    return puzzle[0]


def md5(key, x):
    return hashlib.md5(f'{key}{x}'.encode()).hexdigest()


def part1(key, prefix='00000'):
    i, hash = 0, md5(key, 0)
    while not hash.startswith(prefix):
        i += 1
        hash = md5(key, i)
    return i


def part2(key):
    return part1(key, prefix='000000')


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (609043, None),
        (1048970, None),
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
