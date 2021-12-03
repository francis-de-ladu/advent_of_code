import os
import sys
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    trans_dict = dict(forward=(0, 1), down=(1, 1), up=(1, -1))
    move_tuples = [tuple(entry.split()) for entry in puzzle]
    return [(trans_dict.get(move), int(dist)) for move, dist in move_tuples]


def part1(instructions):
    position = np.asarray([0, 0])
    for ((axis, mult), dist) in instructions:
        position[axis] += mult * dist
    return np.prod(position)


def part2(instructions):
    position, aim = np.asarray([0, 0]), 0
    for ((axis, mult), dist) in instructions:
        if axis == 0:
            position += np.asarray([mult, aim]) * dist
        else:
            aim += mult * dist
    return np.prod(position)


def run_on_input(input_path, solution1=None, solution2=None):
    instructions = prepare_input(input_path)

    answer1 = part1(instructions)
    answer2 = part2(instructions)

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
    solutions = [(150, 900)]

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
