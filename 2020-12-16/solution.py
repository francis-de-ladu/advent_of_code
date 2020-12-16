import os
import re
import sys
from collections import defaultdict
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def run_on_input(input_path, solution1=None, solution2=None):
    fields_dict, ticket, nearby = prepare_input(input_path)

    answer1 = part1(fields_dict, nearby)
    answer2 = part2(fields_dict, ticket, nearby)

    print('\n' + Path(input_path).stem.upper().upper() + ':')
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
        grouped_infos = file.read().split('\n\n')

    fields, ticket, nearby = [group.split('\n') for group in grouped_infos[:3]]

    fields_dict = {}
    for field in fields:
        name, range1, range2 = re.split(r"(?:\:\s|\sor\s)", field)
        min1, max1 = [int(val) for val in range1.split('-')]
        min2, max2 = [int(val) for val in range2.split('-')]
        range1 = set(range(min1, max1 + 1))
        range2 = set(range(min2, max2 + 1))
        fields_dict[name] = range1.union(range2)

    ticket = [int(val) for val in ticket[1].split(',')]
    nearby = [[int(val) for val in entry.split(',')] for entry in nearby[1:-1]]

    return fields_dict, ticket, nearby


def part1(fields_dict, nearby):
    valid_values = set.union(*fields_dict.values())

    invalid = [val for entry in nearby for val in entry
               if val not in valid_values]
    return sum(invalid)


def part2(fields_dict, ticket, nearby):
    valid_values = set.union(*fields_dict.values())

    nearby_valid = [entry for entry in nearby
                    if set(entry).issubset(valid_values)]

    valid_tickets = np.asarray([ticket] + nearby_valid)

    assignments = defaultdict(list)
    for i, pos in enumerate(valid_tickets.T):
        for field, are_valid in fields_dict.items():
            if set(pos).issubset(are_valid):
                assignments[field].append(i)

    assignments = sorted(assignments.items(), key=lambda x: len(x[1]))

    taken_pos = set()
    for _, candidates in assignments:
        [candidates.remove(val) for val in taken_pos if val in candidates]
        assert len(candidates) == 1
        taken_pos.add(candidates[0])

    assignments = [ticket[pos[0]] for field, pos in assignments
                   if field.startswith('departure')]
    return np.prod(assignments).astype(int)


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
    solutions1 = [71, None]
    solutions2 = [None, 1]

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
