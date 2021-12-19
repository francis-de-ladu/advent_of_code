import math
import os
import sys

import numpy as np


def transform(puzzle):
    target = puzzle[0].replace('target area: ', '')
    tx, ty = target.split(', ')
    tx, ty = tx[2:].split('..'), ty[2:].split('..')
    return list(map(int, tx)), list(map(int, ty))


def get_zero(a, b, c):
    return (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)


def part1(data, max_velocity=300):
    target_x, target_y = data

    for v0_y in range(max_velocity, 0, -1):
        a, b, c = 0.5, -v0_y, target_y
        t1, t2 = get_zero(a, b, c[0]), get_zero(a, b, c[1])
        if int(t1) > int(t2):
            # we got an integer time falling in the zone!
            break

    return sum(range(v0_y, 0, -1))


def get_v0_range(target_min, target_max, num_steps, adjustment):
    tg_min, tg_max = target_min + adjustment, target_max + adjustment
    v0_min = math.ceil(tg_min / num_steps)
    v0_max = math.floor(tg_max / num_steps)
    return range(v0_min, v0_max + 1)


def part2(data, max_velocity=300):
    target_x, target_y = data
    (x_min, x_max), (y_min, y_max) = target_x, target_y

    valid_v0_pairs = set()

    # d * (d + 1) / 2 = target  -->  d^2 + d - 2*target = 0
    min_vx = math.ceil(get_zero(1, 1, -2 * x_min))
    max_vx = math.floor(get_zero(1, 1, -2 * x_max))

    # use brute force to find velocity pairs falling in the zone
    # with an x velocity of zero
    for vx in range(min_vx, max_vx + 1):
        for vy in range(abs(y_min)):
            pos_x, pos_y = 0, 0
            curr_vx, curr_vy = vx, vy
            while (pos_x not in range(x_min, x_max + 1) or pos_y not in range(y_min, y_max + 1)) \
                    and pos_x <= x_max and pos_y >= y_min:
                pos_x += curr_vx
                pos_y += curr_vy
                curr_vx = max(0, curr_vx - 1)
                curr_vy -= 1

            if pos_x <= x_max and pos_y >= y_min:
                valid_v0_pairs.add((vx, vy))

    # this adjustment serves to simulate constant velocity (null acceleration)
    adjustment = 0

    for num_steps in np.arange(abs(y_min)) + 1:
        for vx in get_v0_range(x_min, x_max, num_steps, adjustment):
            # if this condition is met, we'll get in the zone
            # for the y-axis after passing it on the x-axis
            if num_steps > vx > max_vx:
                continue

            # get valid y-axis velocities for this number of steps
            for vy in get_v0_range(y_min, y_max, num_steps, adjustment):
                valid_v0_pairs.add((vx, vy))

        adjustment += num_steps

    return len(valid_v0_pairs)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (45, 112),
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
