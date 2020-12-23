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

    @property
    def up(self):
        return ''.join(self.content[0])

    @property
    def down(self):
        return ''.join(self.content[-1])

    @property
    def left(self):
        return ''.join(self.content[:, 0])

    @property
    def right(self):
        return ''.join(self.content[:, -1])

    def flip(self, axis):
        self.content = np.flip(self.content, axis=axis)

    def rotate(self, degrees):
        self.content = np.rot90(self.content, degrees // 90)

    def match_with(self, target, side):
        for _ in range(4):
            if ''.join(self.content[side]) == target:
                return True
            self.rotate(90)

        self.flip(axis=1)

        for _ in range(4):
            if ''.join(self.content[side]) == target:
                return True
            self.rotate(90)

        return False

    def get_sides(self, flipped=False, as_int=False):
        sides = [self.up, self.down, self.left, self.right]
        # for side in ((0, ...), (-1, ...), (..., 0), (..., -1)):
        #     sides.append(''.join(self.content[side]))
        if flipped is True:
            sides = [side[::-1] for side in sides]
        if as_int is True:
            sides = [int(side, 2) for side in sides]
        return sides

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
            # convert sides and flipped sides to int for easier comparison
            side_value = int(side, 2)
            side_flipped = int(side[::-1], 2)
            all_sides[side_value].append(tile_id)
            all_sides[side_flipped].append(tile_id)

    side_tiles = defaultdict(list)
    for side, tile_ids in all_sides.items():
        if len(tile_ids) == 1:
            # if a side only matches one tile, the tile is a side tile
            side_tiles[tile_ids[0]].append(side)

    # corner tiles appear 4 times in `side_tiles`
    # (two sides and their flipped counterpart)
    corner_tiles = set([tile_id for tile_id, sides in side_tiles.items()
                        if len(sides) == 4])

    # build image starting with a corner tile
    image = build_image(tiles, corner_tiles.pop())

    corners = image[(0, 0, -1, -1), (0, -1, 0, -1)]
    answer = np.prod(list(map(lambda tile: tile.id, corners)))

    return answer, image


def build_image(tiles, first_tile):
    image_size = np.sqrt(len(tiles)).astype(int)
    image = np.full([image_size, image_size], None).astype(Tile)

    image[0, 0] = tiles[first_tile]
    del tiles[first_tile]

    for y, x in product(*map(range, image.shape)):
        if (y, x) == (0, 0):
            # first tile has already been placed
            continue

        if x == 0:
            # we'll match with the tile right over it
            prev_tile = image[y - 1, 0]
            target = ''.join(prev_tile.content[-1])
            side = (0, ...)
        else:
            # we'll match with the tile to its left
            prev_tile = image[y, x - 1]
            target = ''.join(prev_tile.content[:, -1])
            side = (..., 0)

        # do until a new tile has been placed
        tile_placed = False
        while not tile_placed:
            for tile_id, tile in list(tiles.items()):
                if not tile.match_with(target, side):
                    # tile doesn't match, continue with next tile
                    continue

                # match found! add to image and remove from unplaced tiles
                image[y, x] = tile
                del tiles[tile_id]

                tile_placed = True
                break
            else:
                assert y in (0, 1)

                if y == 0:
                    # first tile is in a wrong state, rotate it 180 degrees
                    image[0, 0].rotate(180)
                    target = ''.join(prev_tile.content[:, -1])

                if y == 1:
                    # line 0 needs to be flipped vertically
                    for i in range(image_size):
                        image[0, i].flip(axis=0)
                    target = ''.join(prev_tile.content[-1])

    return image


def part2(image):
    # strip contour of every tile
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i, j].content = image[i, j].content[1:-1, 1:-1]

    image_shape = np.asarray(image.shape)
    tile_shape = np.asarray(image[0, 0].content.shape)

    true_image = np.full(image_shape * tile_shape, '')
    for tile_pos in product(*map(np.arange, image.shape)):
        # get slices to select the patch in the true image
        pos_in_image = tile_pos * tile_shape
        patch = map(slice, pos_in_image, pos_in_image + tile_shape)

        # convert to tuples to allow use for indexing
        patch, tile_pos = tuple(patch), tuple(tile_pos)

        # replace patch by the tile content
        true_image[patch] = image[tile_pos].content

    # convert true image from string to int to allow easy comparison
    true_image = true_image.astype(int)

    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]

    # convert monster from string to int to allow easy comparison (3 has been
    # chosen to allow comparison with 1s in the image using binary operators)
    monster = np.vstack([list(line.replace(' ', '0').replace('#', '3'))
                         for line in monster]).astype(int)

    # number of '#' in the mosnter
    monster_value = np.sum(monster) // 3

    for _ in range(4):
        find_monster(true_image, monster, monster_value)
        true_image = np.rot90(true_image)

    true_image = np.flip(true_image, axis=1)

    for _ in range(4):
        find_monster(true_image, monster, monster_value)
        true_image = np.rot90(true_image)

    # # print test in good direction
    # true_image = np.rot90(true_image, 3)
    # true_image = np.flip(true_image, axis=1)
    # for line in true_image.astype(str):
    #     print(''.join(line).replace('0', '.').replace(
    #         '1', '#').replace('3', 'O'))

    # # print puzzle in good direction
    # true_image = np.flip(true_image, axis=1)
    # for line in true_image.astype(str):
    #     print(''.join(line).replace('0', '.').replace(
    #         '1', '#').replace('3', 'O'))

    return np.sum(true_image == 1)


def find_monster(image, monster, monster_value):
    image_shape, monster_shape = map(np.asarray, [image.shape, monster.shape])
    for pos in product(*map(np.arange, image_shape - monster_shape)):
        pos = tuple(map(slice, pos, pos + monster_shape))
        if np.sum(np.clip(image[pos] & monster, 0, 1)) == monster_value:
            image[pos] = image[pos] | monster


def run_on_input(input_path, solution1=None, solution2=None):
    tiles = prepare_input(input_path)

    answer1, image = part1(tiles)
    answer2 = part2(image)

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
