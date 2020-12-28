import os
import sys
from os.path import abspath, dirname
from pathlib import Path


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    door_pub, card_pub = map(int, puzzle)
    return door_pub, card_pub


def part1(door_pub, card_pub):
    print(door_pub, card_pub)

    mod_value = 20201227
    subject_num = 7

    card_value = 1
    door_value = 1

    card_loop = 0
    while card_value != card_pub:
        card_value *= subject_num
        card_value %= mod_value
        card_loop += 1

    door_loop = 0
    while door_value != door_pub:
        door_value *= subject_num
        door_value %= mod_value
        door_loop += 1

    card_value = 1
    door_value = 1

    [card_value := card_value * door_pub % mod_value for i in range(card_loop)]
    [door_value := door_value * card_pub % mod_value for i in range(door_loop)]
    assert card_value == door_value

    return card_value


def part2():
    return


def run_on_input(input_path, solution1=None, solution2=None):
    door_pub, card_pub = prepare_input(input_path)

    answer1 = part1(door_pub, card_pub)
    answer2 = part2()

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
    solutions = [(14897079, None)]

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
