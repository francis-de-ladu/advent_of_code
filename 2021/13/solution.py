import os
import sys
from itertools import product

import numpy as np


def transform(puzzle):
    split_idx = puzzle.index('')
    dots, instrs = puzzle[:split_idx], puzzle[split_idx + 1:]

    dots = np.asarray([dot.split(',') for dot in dots]).astype(int)
    instrs = [tuple(instr) for instr in map(lambda i: i.split('='), instrs)]

    return dots, instrs


def fold_paper(dots, instr):
    axis, pos = int(instr[0] == 'fold along y'), int(instr[1])
    dots[:, axis] = np.where(dots[:, axis] > pos,
                             dots[:, axis] - 2 * (dots[:, axis] - pos),
                             dots[:, axis])

    return np.unique(dots, axis=0)


def part1(data):
    dots, instrs = data
    dots = fold_paper(dots, instrs[0])
    return len(dots)


def part2(data):
    dots, instrs = data
    for instr in instrs:
        dots = fold_paper(dots, instr)

    folded_paper = np.ndarray(np.max(dots, axis=0) + 1).astype(str)
    folded_paper.fill('.')
    folded_paper[tuple(zip(*dots))] = '#'
    folded_paper = folded_paper.T

    for line in list(map(''.join, folded_paper.tolist())):
        print(line)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (17, None),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
