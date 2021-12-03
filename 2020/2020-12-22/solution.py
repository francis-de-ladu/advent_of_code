import os
import sys
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().split('\n')

    player1 = []
    while card := puzzle.pop(1):
        player1.append(int(card))

    player2 = []
    while card := puzzle.pop(2):
        player2.append(int(card))

    return player1, player2


def part1(player1, player2):
    # create copies to avoid modifying decks from the outer scope
    player1, player2 = player1.copy(), player2.copy()

    while len(player1) and len(player2):
        p1, p2 = player1.pop(0), player2.pop(0)
        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    winner = np.asarray(player1 if len(player1) else player2)[::-1]
    card_values = np.arange(len(winner)) + 1

    return np.sum(winner * card_values)


def part2(player1, player2):
    player1, player2, p1_wins = \
        part2_helper(player1.copy(), player2.copy())

    winner = np.asarray(player1 if p1_wins else player2)[::-1]
    card_values = np.arange(len(winner)) + 1

    return np.sum(winner * card_values)


def part2_helper(player1, player2):
    # to store seen configs
    seen_configs = set()

    while len(player1) and len(player2):
        # end loop if the config has already happened, else add to seen configs
        current_config = str([player1, player2])
        if current_config in seen_configs:
            break
        seen_configs.add(current_config)

        # draw cards
        p1, p2 = player1.pop(0), player2.pop(0)

        # start sub-game if condition is met, otherwise check who wins
        if p1 <= len(player1) and p2 <= len(player2):
            _, _, p1_wins = \
                part2_helper(player1[:p1].copy(), player2[:p2].copy())
        else:
            p1_wins = p1 > p2

        # add cards to winner's deck
        if p1_wins:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    p1_wins = True if len(player1) else False
    return player1, player2, p1_wins


def run_on_input(input_path, solution1=None, solution2=None):
    player1, player2 = prepare_input(input_path)

    answer1 = part1(player1, player2)
    answer2 = part2(player1, player2)

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
    solutions = [(306, 291)]

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
