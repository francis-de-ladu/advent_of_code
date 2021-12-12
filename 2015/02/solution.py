import math
import os
import sys


class Box():
    def __init__(self, dimensions):
        self.l, self.w, self.h = map(int, dimensions.split('x'))

    def get_area(self):
        return 2 * (self.l * self.w + self.w * self.h + self.h * self.l)

    def get_smallest_area(self):
        return math.prod(sorted([self.l, self.w, self.h])[:2])

    def get_smallest_perim(self):
        return 2 * sum(sorted([self.l, self.w, self.h])[:2])

    def get_volume(self):
        return math.prod([self.l, self.w, self.h])


def transform(puzzle):
    return [Box(dimensions) for dimensions in puzzle]


def part1(data):
    return sum(box.get_area() + box.get_smallest_area() for box in data)


def part2(data):
    return sum(box.get_smallest_perim() + box.get_volume() for box in data)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (58, 34),
        (43, 14),
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
