import os
import sys
from collections import defaultdict
from itertools import repeat


class Line():
    def __init__(self, entry):
        self.p1, self.p2 = map(Point, entry.split(' -> '))

        self.x_range, self.y_range = self.get_range('x'), self.get_range('y')
        if isinstance(self.x_range, int):
            self.x_range = list(repeat(self.x_range, len(self.y_range)))
        elif isinstance(self.y_range, int):
            self.y_range = list(repeat(self.y_range, len(self.x_range)))

    def get_delta(self, attr):
        return getattr(self.p2, attr) - getattr(self.p1, attr)

    def get_step(self, attr):
        delta = self.get_delta(attr)
        return delta // abs(delta) if delta else 0

    def get_range(self, attr):
        step = self.get_step(attr)
        p1, p2 = getattr(self.p1, attr), getattr(self.p2, attr)
        return list(range(p1, p2 + step, step)) if step else p1

    def is_straight(self):
        return self.p1.x == self.p2.x or self.p1.y == self.p2.y

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
    for line in filter(lambda l: l.is_straight(), data):
        for coord in zip(line.x_range, line.y_range):
            ocean_floor[coord] += 1

    return len(list(filter(lambda pos: pos > 1, ocean_floor.values())))


def part2(data):
    ocean_floor = defaultdict(int)
    for line in data:
        for coord in zip(line.x_range, line.y_range):
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
