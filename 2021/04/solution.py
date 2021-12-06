import os
import re
import sys

import numpy as np


def transform(puzzle):
    numbers = list(map(int, puzzle[0].split(',')))
    boards = ','.join(puzzle[2:]).split(',,')
    boards = np.asarray(
        [[[int(number)
           for number in re.split(r'\s+', row.strip())]
          for row in board.split(',')]
         for board in boards]
    )
    return numbers, boards


def draw_numbers(data, end_condition):
    numbers, boards = data
    marked_numbers = np.zeros_like(boards).astype(bool)
    won_on_lines = np.zeros(boards.shape[0]).astype(bool)
    won_on_columns = np.zeros(boards.shape[0]).astype(bool)

    for number in numbers:
        # mark drawn number on boards
        marked_numbers |= (boards == number)

        # check winnning statuses
        have_won_on_lines = np.any(np.all(marked_numbers, axis=1), axis=1)
        have_won_on_columns = np.any(np.all(marked_numbers, axis=2), axis=1)

        # check end condition
        if end_condition(have_won_on_lines | have_won_on_columns):
            had_already_won = won_on_lines | won_on_columns
            have_just_won = have_won_on_lines | have_won_on_columns
            index = np.argmax(had_already_won != have_just_won)
            board_sum = np.sum(boards[index] * ~marked_numbers[index])
            return number * board_sum

        # update winning statuses
        won_on_lines |= have_won_on_lines
        won_on_columns |= have_won_on_columns


def part1(data):
    return draw_numbers(data, end_condition=any)


def part2(data):
    return draw_numbers(data, end_condition=all)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (4512, 1924),
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
