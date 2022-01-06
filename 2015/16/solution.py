import os
import re
import sys
from operator import eq, gt, lt


def transform(puzzle):
    pattern = re.compile(r'[:,]?\s')
    entries = [re.split(pattern, line)[2:] for line in puzzle]
    entries = [zip(entry[::2], map(int, entry[1::2])) for entry in entries]
    entries = [dict(entry) for entry in entries]
    return entries


def read_ticker_tape():
    return dict(
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )


def part1(data):
    ticker_tape = read_ticker_tape()
    for i, aunt in enumerate(data):
        for compound, quantity in ticker_tape.items():
            if aunt.get(compound, quantity) != quantity:
                break
        else:
            return i + 1


def part2(data):
    ticker_tape = read_ticker_tape()
    ops = dict(cats=gt, trees=gt, pomeranians=lt, goldfish=lt)
    for i, aunt in enumerate(data):
        for compound, quantity in ticker_tape.items():
            op = ops.get(compound, eq)
            if compound in aunt and not op(aunt[compound], quantity):
                break
        else:
            return i + 1


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
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
