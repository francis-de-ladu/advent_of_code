import os
import sys
from os.path import abspath, basename, dirname

# from helpers import submit_solution


def run_on_input(input_path, solution1=None, solution2=None):
    _ = prepare_input(input_path)

    answer1 = part1()
    answer2 = part2()

    print('\n' + basename(input_path).upper() + ':')
    print("Part1:", answer1)
    print("Part2:", answer2)

    if answer1:
        assert solution1 is None or answer1 == solution1, \
            f"got answer {answer1} for part 1, but was expeting {solution1}"

    if answer1 and answer2:
        assert solution2 is None or answer2 == solution2, \
            f"got answer {answer2} for part 2, but was expeting {solution2}"

    return answer1, answer2


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    return puzzle


def part1():
    return


def part2():
    return


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
    solutions1 = []
    solutions2 = []

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    for entry, sol1, sol2 in zip(dir_scanner, solutions1, solutions2):
        run_on_input(entry.path, sol1, sol2)

    # run on input puzzle
    answer1, answer2 = run_on_input(f"{directory}/puzzle.txt")
    print()

    # if you got here, all went well with tests, so submit solution
    year, _, day = directory.split('-')
    if answer2 is None:
        submit_solution(year, day, answer1, level=1)
    else:
        submit_solution(year, day, answer2, level=2)
