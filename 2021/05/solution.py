import os
import sys
from collections import defaultdict

import numpy as np


def get_range(line, attr):
    start, end = getattr(line.p1, attr), getattr(line.p2, attr)
    delta = end - start
    step = delta // abs(delta) if delta != 0 else 1
    return list(range(start, end + step, step))


class Line():
    def __init__(self, entry):
        self.p1, self.p2 = map(Point, entry.split(' -> '))
        self.x_max = max(self.p1.x, self.p2.x)
        self.y_max = max(self.p1.y, self.p2.y)

        self.x_range, self.y_range = get_range(self, 'x'), get_range(self, 'y')
        x_len, y_len = len(self.x_range), len(self.y_range)

        if x_len > 1 and y_len == 1:
            self.y_range = x_len * self.y_range
        elif y_len > 1 and x_len == 1:
            self.x_range = y_len * self.x_range

    def is_diagonal(self):
        return self.p1.x != self.p2.x and self.p1.y != self.p2.y

    def __str__(self):
        return f'{self.p1} -> {self.p2}'


class Point():
    def __init__(self, raw):
        self.x, self.y = map(int, raw.split(','))

    def __str__(self):
        return f'({self.x}, {self.y})'


def transform(puzzle):
    return [Line(entry) for entry in puzzle]


def part1(data):
    ocean_floor = defaultdict(int)
    for line in filter(lambda l: not l.is_diagonal(), data):
        for coord in zip(line.y_range, line.x_range):
            ocean_floor[coord] += 1

    return len(list(filter(lambda pos: pos > 1, ocean_floor.values())))


def part2(data):
    ocean_floor = defaultdict(int)
    for line in data:
        for coord in zip(line.y_range, line.x_range):
            ocean_floor[coord] += 1

    return len(list(filter(lambda pos: pos > 1, ocean_floor.values())))


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (5, 12),
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
