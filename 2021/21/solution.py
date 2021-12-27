import os
import sys
from collections import defaultdict
from itertools import product

import numpy as np


def transform(puzzle):
    strip_len = len('Player 1 starting position: ')
    return [int(line[strip_len:]) for line in puzzle]


def part1(positions, num_spaces=10, num_rolls=3, target=1000, faces=100):
    positions = [pos for pos in positions]
    scores = [0 for _ in positions]

    turn_cnt = 0
    next_roll = 0
    while max(scores) < target:
        for i, pos in enumerate(positions):
            rolls = np.arange(next_roll, next_roll + num_rolls) % faces + 1
            positions[i] = (pos + sum(rolls) - 1) % num_spaces + 1
            scores[i] += positions[i]

            next_roll = (next_roll + num_rolls) % faces
            turn_cnt += 1

            if scores[i] >= target:
                break

    return min(scores) * turn_cnt * 3


def part2(positions, num_spaces=10, num_rolls=3, target=21, faces=3):
    outcomes = np.sum(list(product(np.arange(faces) + 1, repeat=3)), axis=1)
    outcomes, freqs = np.unique(outcomes, axis=0, return_counts=True)

    players = []
    for pos in positions:
        games = defaultdict(int)
        finished = []

        score, turn = 0, 0
        games[(pos, score)] = 1

        while len(games):
            finished.append(0)
            new_games = defaultdict(int)
            for (pos, score), num_games in games.items():
                new_positions = (pos + outcomes - 1) % num_spaces + 1
                for new_pos, freq in zip(new_positions, freqs):
                    new_score = score + new_pos
                    new_num_games = num_games * freq
                    if new_score >= target:
                        finished[-1] += new_num_games
                    else:
                        new_games[(new_pos, new_score)] += new_num_games

            games = new_games

        players.append(finished)

    wins = [0 for _ in players]
    universes = [1 for _ in players]
    for turn, num_wins in enumerate(sum(zip(*players), ())):
        player = turn % 2
        other = (turn + 1) % 2
        universes[player] = universes[player] * faces**faces - num_wins
        wins[player] += num_wins * universes[other]

    return max(wins)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (739785, 444356092776315),
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
