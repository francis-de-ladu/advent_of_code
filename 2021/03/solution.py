import os
import sys

import numpy as np


def transform(puzzle):
    return np.stack([list(entry) for entry in puzzle], axis=0).astype(int)


def part1(bits):
    means = np.mean(bits, axis=0)
    gamma = int(''.join((means >= 0.5).astype(int).astype(str)), base=2)
    epsilon = int(''.join((means < 0.5).astype(int).astype(str)), base=2)
    return gamma * epsilon


def part2(bits):
    ids_oxy = np.arange(bits.shape[0])
    ids_co2 = np.arange(bits.shape[0])
    for i in range(bits.shape[1]):
        # oxygen generator
        if len(ids_oxy) > 1:
            support = np.ones_like(ids_oxy) * i
            mc_bit = 0 if np.mean(bits[ids_oxy, support]) >= 0.5 else 1
            ids_oxy = np.asarray(
                [id for id in ids_oxy if bits[id, i] == mc_bit])
        # co2 scrubber
        if len(ids_co2) > 1:
            support = np.ones_like(ids_co2) * i
            lc_bit = 1 if np.mean(bits[ids_co2, support]) >= 0.5 else 0
            ids_co2 = np.asarray(
                [id for id in ids_co2 if bits[id, i] == lc_bit])

    bits_str = bits.astype(str)
    bits_numbers = np.stack([int(''.join(line), base=2) for line in bits_str])
    oxy_rating = bits_numbers[ids_oxy[0]]
    co2_rating = bits_numbers[ids_co2[0]]
    return oxy_rating * co2_rating


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    p1_solutions = [198]
    p2_solutions = [230]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        p1_solutions=p1_solutions,
        p2_solutions=p2_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
