import os
import sys
from itertools import product
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def prepare_input(input_path, num_cycles):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    puzzle = [[1 if cube == '#' else 0 for cube in list(line)]
              for line in puzzle]
    puzzle = np.expand_dims(np.asarray(puzzle), axis=0)
    # print(puzzle)

    grid = np.zeros(np.asarray(puzzle.shape) + 2 * num_cycles, dtype=np.int)

    pos = slice(num_cycles, -num_cycles)
    grid[pos, pos, pos] = puzzle
    # print(grid)

    return grid


def part1(grid, num_cycles):
    for i in range(num_cycles):
        active_neighbs = np.zeros_like(grid)
        for pos in product(*map(range, grid.shape)):
            pos = tuple(pos)
            n_hood = tuple(map(lambda p: slice(max(0, p - 1), p + 2), pos))
            active_neighbs[pos] = np.sum(grid[n_hood]) - grid[pos]
        grid = np.where(grid, np.isin(active_neighbs, [2, 3]),
                        active_neighbs == 3).astype(int)

    return np.sum(grid)


def part2():
    return


def run_on_input(input_path, solution1=None, solution2=None):
    num_cycles = 6
    grid = prepare_input(input_path, num_cycles)

    answer1 = part1(grid, num_cycles)
    new_grid = np.zeros((2 * num_cycles + 1,) + grid.shape)
    new_grid[num_cycles] = grid
    answer2 = part1(new_grid, num_cycles)

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

    # test solutions
    solutions1 = [112]
    solutions2 = [848]

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    for entry, sol1, sol2 in zip(dir_scanner, solutions1, solutions2):
        run_on_input(entry.path, sol1, sol2)

    # run on input puzzle
    answer1, answer2 = run_on_input(f"{directory}/puzzle.txt")
    print()

    # if you got here, all went well with tests, so submit solution
    year, _, day = directory.split('-')
    if answer2 is not None:
        submit_solution(year, day, answer2, part=2)
    elif answer1 is not None:
        submit_solution(year, day, answer1, part=1)
    else:
        print("There was no answer to submit...")
