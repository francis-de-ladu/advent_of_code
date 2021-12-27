import math
import os
import sys
from itertools import product


def transform(puzzle):
    data = []
    for line in puzzle:
        instr, cube = line.split()
        ranges = [map(int, coord[2:].split('..')) for coord in cube.split(',')]
        data.append(
            (instr, tuple([range(beg, end + 1) for beg, end in ranges])))

    return data


def part1(data, threshold=50):
    reactor = set()
    for instr, cube in data:
        if any(map(lambda r: r.start < -threshold or r.stop - 1 > threshold, cube)):
            continue

        for pos in product(*cube):
            reactor.add(pos) if instr == 'on' else reactor.discard(pos)

    return len(reactor)


def run_step(instr, cube, reactor):
    for area in reactor.copy():
        if all(map(is_overlapping, cube, area)):
            reactor.remove(area)
            for new_area in strip_from(area, cube):
                reactor.add(new_area)

    if instr == 'on':
        reactor.add(cube)

    return reactor


def is_overlapping(range1, range2):
    return range1.start <= range2.stop and range2.start <= range1.stop


def strip_from(area, cube):
    new_areas = []
    for idx, (area_axis, cube_axis) in enumerate(zip(area, cube)):
        if area_axis.start < cube_axis.start:
            new_areas.append(
                insert_range(area, idx, area_axis.start, cube_axis.start))
        if cube_axis.stop < area_axis.stop:
            new_areas.append(
                insert_range(area, idx, cube_axis.stop, area_axis.stop))

        new_start = max(area_axis.start, cube_axis.start)
        new_stop = min(area_axis.stop, cube_axis.stop)
        area = insert_range(area, idx, new_start, new_stop)

    return new_areas


def insert_range(area, idx, start, stop):
    return area[:idx] + (range(start, stop),) + area[idx + 1:]


def part2(data):
    reactor = set()
    for instr, cube in data:
        reactor = run_step(instr, cube, reactor)

    num_lit = 0
    for area in reactor:
        num_lit += math.prod(map(len, area))

    return num_lit


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (39, 39),
        (590784, None),
        (474140, 2758514936282235),
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
