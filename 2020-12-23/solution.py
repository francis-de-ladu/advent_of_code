import copy
import os
import sys
from os.path import abspath, dirname
from pathlib import Path


class Cup(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    puzzle = [int(value) for value in puzzle[0]]

    cups = {value: Cup(value) for value in puzzle}

    cups1 = list(cups.values())
    cups2 = cups1[1:] + [cups1[0]]

    for cup1, cup2 in zip(cups1, cups2):
        cup1.right, cup2.left = cup2, cup1

    return cups, puzzle[0]


def part1(cups, current, num_moves, full_state=False):
    for i in range(num_moves):
        removed = cups[current].right
        cups[current].right = cups[current].right.right.right.right
        cups[current].right.left = cups[current]

        cup = removed
        removed_values = set()
        for _ in range(3):
            removed_values.add(cup.value)
            cup = cup.right

        dest = current
        while (dest := sub1(dest, len(cups))) in removed_values:
            pass

        cups[dest].right.left = removed.right.right.right
        removed.right.right.right = cups[dest].right
        cups[dest].right, removed.left = removed, cups[dest]

        current = cups[current].right.value

    final_state = print_state(cups, current=1, return_state=True)

    if full_state:
        return final_state

    return ''.join(final_state[1:])


def print_state(cups, current, return_state=False):
    cup = cups[current]

    state = []
    for i in range(len(cups)):
        state.append(str(cup.value))
        cup = cup.right

    if return_state:
        return state

    state = '-'.join(state)
    print(state)


def sub1(value, num_cups):
    value -= 1
    if value == 0:
        value += num_cups
    return value


def part2(cups, current, num_moves):
    prev = list(cups.values())[-1]
    while prev.value < 1000000:
        next_value = len(cups) + 1
        next_cup = Cup(next_value)
        cups[next_cup.value] = next_cup
        prev.right, next_cup.left = next_cup, prev
        prev = next_cup

    cups[current].left, prev.right = prev, cups[current]

    final_state = part1(cups, current, num_moves, full_state=True)
    return str(int(final_state[1]) * int(final_state[2]))


def run_on_input(input_path, solution1=None, solution2=None):
    cups, current = prepare_input(input_path)

    answer1 = part1(copy.deepcopy(cups), current, num_moves=100)
    print(answer1)
    answer2 = part2(copy.deepcopy(cups), current, num_moves=10000000)

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
    solutions = [('67384529', '149245887792')]

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
