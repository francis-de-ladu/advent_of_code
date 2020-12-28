import os
import sys
from collections import defaultdict
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    instructions = [list(line) for line in puzzle]
    return instructions


def part1(instructions):
    move = {'e': [1.0, 0.0], 'w': [-1.0, 0.0],
            'ne': [0.5, 0.5], 'sw': [-0.5, -0.5],
            'nw': [-0.5, 0.5], 'se': [0.5, -0.5]}
    move = {key: np.asarray(value) for key, value in move.items()}

    black_tiles = defaultdict(bool)
    for line in instructions:
        current_pos = np.asarray([0.0, 0.0])
        while len(line) > 0:
            direction = line.pop(0)
            if direction in "ns":
                direction += line.pop(0)

            current_pos += move[direction]

        pos_key = tuple(current_pos)
        black_tiles[pos_key] = not black_tiles[pos_key]

    num_black = sum(black_tiles.values())
    return num_black, move, black_tiles


def part2(move, black_tiles):
    # make sure every tile in the starting floor exists in the dict
    minimums = np.min(list(black_tiles.keys()), axis=0)
    maximums = np.max(list(black_tiles.keys()), axis=0)
    for i in np.arange(minimums[0] - 1, maximums[0] + 1.5, 0.5):
        for j in np.arange(minimums[1] - 1, maximums[1] + 1.5, 0.5):
            black_tiles[(i, j)]

    for day in range(100):
        to_flip = []

        for pos, is_black in list(black_tiles.items()):
            black_neighbours = sum([black_tiles[tuple(pos + dir)]
                                    for dir in move.values()])

            if is_black and black_neighbours in (0, 3, 4, 5, 6):
                to_flip.append(pos)
            elif not is_black and black_neighbours == 2:
                to_flip.append(pos)

        for pos in map(tuple, to_flip):
            black_tiles[pos] = not black_tiles[pos]

    num_black = sum(black_tiles.values())
    return num_black


def run_on_input(input_path, solution1=None, solution2=None):
    instructions = prepare_input(input_path)

    answer1, move, black_tiles = part1(instructions)
    answer2 = part2(move, black_tiles)

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
    solutions = [(10, 2208)]

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    test_paths = sorted([entry.path for entry in dir_scanner])
    for path, (sol1, sol2) in zip(test_paths, solutions):
        run_on_input(path, sol1, sol2)

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
