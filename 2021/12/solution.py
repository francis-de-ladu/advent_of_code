import os
import sys
from collections import defaultdict


def transform(puzzle):
    caves = defaultdict(set)
    for c1, c2 in map(lambda path: path.split('-'), puzzle):
        caves[c1].add(c2)
        caves[c2].add(c1)

    visits_left = {c: float('inf') if c.isupper() else 1 for c in caves}
    return caves, visits_left


def explore(current, caves, visits_left, path_cnt, can_revisit):
    if current == 'end':
        return path_cnt + 1

    visits_left[current] -= 1
    for cave in caves[current]:
        if visits_left[cave] > 0 or can_revisit and cave not in ('start', 'end'):
            path_cnt = explore(cave, caves, visits_left.copy(), path_cnt,
                               can_revisit if visits_left[cave] > 0 else False)

    return path_cnt


def part1(data, can_revisit=False):
    caves, visits_left = data
    return explore('start', caves, visits_left.copy(), path_cnt=0, can_revisit=can_revisit)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(can_revisit=True)

    # solutions to examples given for validation
    test_solutions = [
        (10, 36),
        (19, 103),
        (226, 3509),
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
