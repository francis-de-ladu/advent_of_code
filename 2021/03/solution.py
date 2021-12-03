import os
import sys
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()
        puzzle = np.stack([list(entry) for entry in puzzle], axis=0)

    return puzzle.astype(int)


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


def run_on_input(input_path, solution1=None, solution2=None):
    bits = prepare_input(input_path)

    answer1 = part1(bits)
    answer2 = part2(bits)

    print('\n' + Path(input_path).stem.upper() + ':')
    print("Part1:", answer1)
    print("Part2:", answer2)

    if answer1 is not None:
        assert solution1 is None or answer1 == solution1, \
            f"got answer {answer1} for part 1, but was expeting {solution1}"

    if answer1 is not None and answer2 is not None:
        assert solution2 is None or answer2 == solution2, \
            f"got answer {answer2} for part 2, but was expeting {solution2}"

    return answer1, answer2


if __name__ == "__main__":
    # need to add parent directory to path before importing from helpers
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from helpers import submit_solution

    # get path used to come here
    file_path = sys.argv[0]

    # get name of the directory where this file sits
    directory = os.path.split(dirname(file_path))[1]
    if not directory:
        directory = os.path.split(dirname(abspath(file_path)))[1]

    # test solutions (one tuple per test -> (part1, part2))
    solutions = [(198, 230)]

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    test_paths = sorted([entry.path for entry in dir_scanner])
    for path, (sol1, sol2) in zip(test_paths, solutions):
        run_on_input(path, sol1, sol2)

    # run on input puzzle
    answer1, answer2 = run_on_input(f"{directory}/puzzle.txt")
    print()

    # if you got here, all went well with tests, so submit solution
    year, _, day = map(int, directory.split('-'))
    if answer2 is not None:
        submit_solution(year, day, answer2, part=2)
    elif answer1 is not None:
        submit_solution(year, day, answer1, part=1)
    else:
        print("There was no answer to submit...")
