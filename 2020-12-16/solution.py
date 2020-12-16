import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def run_on_input(input_path):
    fields_dict, ticket, nearby = prepare_input(input_path)

    print('\n' + Path(input_path).stem.upper() + ':')
    print("Part1:", part1(fields_dict, nearby))
    print("Part2:", part2(fields_dict, ticket, nearby))


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
    # get the directory where this file sits
    directory = os.path.dirname(sys.argv[0]) or '.'

    # tests
    for entry in os.scandir(f"{directory}/tests"):
        run_on_input(entry.path)

    # puzzle
    run_on_input(f"{directory}/puzzle.txt")
    print()
