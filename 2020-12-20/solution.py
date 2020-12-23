import os
import re
import sys
import time
from collections import defaultdict
from itertools import product
from os.path import abspath, dirname
from pathlib import Path

import numpy as np


class Tile(object):
    def __init__(self, id, tile):
        self.id = id
        self.content = tile

    def flip(self, axis):
        self.content = np.flip(self.content, axis=axis)

    def rotate(self, degrees):
        self.content = np.rot90(self.content, degrees // 90)

    def match_with(self, config, side):
        for _ in range(4):
            if ''.join(self.content[side]) == config:
                return True
            self.rotate(90)

        self.flip(axis=1)

        for _ in range(4):
            if ''.join(self.content[side]) == config:
                return True
            self.rotate(90)

        return False

    def get_sides(self, flipped=False, as_int=False):
        sides = []
        for side in ((0, ...), (-1, ...), (..., 0), (..., -1)):
            sides.append(''.join(self.content[side]))
        if flipped is True:
            sides = [side[::-1] for side in sides]
        if as_int is True:
            sides = [int(side, 2) for side in sides]
        return sides

    # def get_content(self):
    #     return self.content[1:-1, 1:-1]

    def __repr__(self):
        return f"Tile {self.id}"


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().replace('#', '1').replace('.', '0')[:-1]
        entries = puzzle.split('\n\n')

    entries = [re.sub(r"[^\d]+(\d+):", r"\1", entry).split('\n')
               for entry in entries]

    tiles = {int(entry[0]): np.vstack([list(line) for line in entry[1:]])
             for entry in entries}

    tiles = {tile_id: Tile(tile_id, tile) for tile_id, tile in tiles.items()}

    return tiles


def part1(tiles):
    tile_sides = {tile.id: tile.get_sides() for tile in tiles.values()}

    all_sides = defaultdict(list)
    for tile_id, sides in tile_sides.items():
        for side in sides:
            side_value = int(side, 2)
            side_flipped = int(side[::-1], 2)
            all_sides[side_value].append(tile_id)
            all_sides[side_flipped].append(tile_id)

    side_tiles = defaultdict(list)
    for side, tile_ids in all_sides.items():
        if len(tile_ids) == 1:
            side_tiles[tile_ids[0]].append(side)

    corner_tiles = set([tile_id for tile_id, sides in side_tiles.items()
                        if len(sides) == 4])

    board = build_board(tiles, corner_tiles.pop())

    corners = board[(0, 0, -1, -1), (0, -1, 0, -1)]
    answer = np.prod(list(map(lambda tile: tile.id, corners)))

    return answer, board


def build_board(tiles, first_tile):
    board_length = np.sqrt(len(tiles)).astype(int)
    board = np.full([board_length, board_length], None).astype(Tile)

    board[0, 0] = tiles[first_tile]
    del tiles[first_tile]

    for y, x in product(*map(range, board.shape)):
        if (y, x) == (0, 0):
            continue

        if x == 0:
            prev = board[y - 1, 0]
            config = ''.join(prev.content[-1])
            side = (0, ...)
        else:
            prev = board[y, x - 1]
            config = ''.join(prev.content[:, -1])
            side = (..., 0)

        line_done = False
        while not line_done:
            for tile_id, tile in list(tiles.items()):
                if not tile.match_with(config, side):
                    continue

                board[y, x] = tile
                del tiles[tile_id]

                line_done = True
                break
            else:
                assert y in (0, 1)

                if y == 0:
                    # first tile has been placed in a wrong state
                    board[0, 0].rotate(180)
                    config = ''.join(prev.content[:, -1])

                if y == 1:
                    # line 0 needs to be flipped vertically
                    for i in range(board_length):
                        board[0, i].flip(axis=0)
                    config = ''.join(prev.content[-1])

    return board


def part2(board):
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            board[i, j].content = board[i, j].content[1:-1, 1:-1]

    board_shape = np.asarray(list(board.shape))
    tile_shape = np.asarray(list(board[0, 0].content.shape))

    true_board = np.full(board_shape * tile_shape, '')
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            start = np.asarray([i, j]) * tile_shape
            end = np.asarray([i + 1, j + 1]) * tile_shape
            true_board[start[0]:end[0], start[1]:end[1]] = board[i, j].content

    true_board = true_board.astype(int)

    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]

    monster = np.vstack([list(line.replace(' ', '0').replace('#', '3'))
                         for line in monster]).astype(int)

    monster_value = np.sum(monster) // 3

    for _ in range(4):
        find_monster(true_board, monster, monster_value)
        true_board = np.rot90(true_board)

    true_board = np.flip(true_board, axis=1)

    for _ in range(4):
        find_monster(true_board, monster, monster_value)
        true_board = np.rot90(true_board)

    # # print test in good direction
    # true_board = np.rot90(true_board, 3)
    # true_board = np.flip(true_board, axis=1)
    # for line in true_board.astype(str):
    #     print(''.join(line).replace('0', '.').replace(
    #         '1', '#').replace('3', 'O'))

    # # print puzzle in good direction
    # true_board = np.flip(true_board, axis=1)
    # for line in true_board.astype(str):
    #     print(''.join(line).replace('0', '.').replace(
    #         '1', '#').replace('3', 'O'))

    return np.sum(true_board == 1)


def find_monster(board, monster, monster_value):
    for i in range(board.shape[0] - monster.shape[0]):
        for j in range(board.shape[1] - monster.shape[1]):
            pos = tuple([slice(i, i + monster.shape[0]),
                         slice(j, j + monster.shape[1])])
            if np.sum(np.clip(board[pos] & monster, 0, 1)) == monster_value:
                board[pos] = board[pos] | monster


def run_on_input(input_path, solution1=None, solution2=None):
    tiles = prepare_input(input_path)

    answer1, board = part1(tiles)
    answer2 = part2(board)

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
    solutions = [(20899048083289, 273)]

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
