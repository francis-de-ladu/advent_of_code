import os
import re
import sys

import numpy as np


def transform(puzzle):
    pattern = re.compile(r',?\s')
    return [re.split(pattern, line) for line in puzzle]


def part1(program, register_a_initial=0):
    registers = dict(a=register_a_initial, b=0)

    pc = 0
    while pc < len(program):
        instr, *operands = program[pc]

        if instr == 'hlf':
            registers[operands[0]] //= 2
        elif instr == 'tpl':
            registers[operands[0]] *= 3
        elif instr == 'inc':
            registers[operands[0]] += 1
        elif instr == 'jmp':
            pc += int(operands[0]) - 1
        elif instr == 'jie' and registers[operands[0]] % 2 == 0:
            pc += int(operands[1]) - 1
        elif instr == 'jio' and registers[operands[0]] == 1:
            pc += int(operands[1]) - 1

        pc += 1

    return registers['b']


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(register_a_initial=1)

    # solutions to examples given for validation
    test_solutions = [
        (False, False),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
