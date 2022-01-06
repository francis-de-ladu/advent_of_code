import os
import sys
from collections import defaultdict


def transform(puzzle):
    molecule = puzzle.pop()
    puzzle.pop()

    trans_table = [line.split(' => ') for line in puzzle]
    return molecule, trans_table


def part1(data):
    molecule, trans_table = data
    new_molecules = set()

    replacements = defaultdict(set)
    for elem, repl in trans_table:
        replacements[elem].add(repl)

    for element in replacements.keys():
        elem_len = len(element)
        for repl in replacements[element]:
            for i, _ in enumerate(molecule):
                if element == molecule[i:i + elem_len]:
                    new_molecules.add(
                        molecule[:i] + repl + molecule[i + elem_len:])

    return len(new_molecules)


def attempt_replacement(molecule, replacements, num_steps=0):
    if molecule == 'e':
        return num_steps

    for repl in sorted(replacements.keys(), reverse=True, key=len):
        if repl not in molecule:
            continue

        new_molecule = molecule.replace(repl, replacements[repl])
        new_num_steps = attempt_replacement(
            new_molecule, replacements, num_steps + molecule.count(repl))

        if new_num_steps is not None:
            return new_num_steps


def part2(data):
    molecule, trans_table = data
    replacements = dict(map(lambda x: x[::-1], trans_table))
    return attempt_replacement(molecule, replacements)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (4, 3),
        (7, 6),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
