import os
import sys
from collections import defaultdict, namedtuple
from queue import PriorityQueue

import numpy as np

# named tuple for a position in the burrow
Pos = namedtuple('Pos', 'y x')


class Room:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.cost = 10**(ord(name) - 65)

    def is_open(self, burrow):
        return set(burrow[:, self.pos]).issubset({'.', '#', self.name})


def transform(puzzle):
    width = len(puzzle[0])
    burrow = np.stack([list(line.ljust(width)) for line in puzzle])
    return burrow


def find_solution(situations, rooms, part=1):
    already_seen = set()
    while not situations.empty():
        (min_energy, energy), burrow = situations.get()
        burrow = np.vstack(burrow)
        if energy > 0 and set(burrow[1]) == set(['.', '#']):
            return energy

        # find candidates for amphipods in hallway
        for x in range(1, len(burrow[0]) - 1):
            find_candidates(
                burrow, rooms, Pos(1, x), energy,  situations, already_seen)

        # find candidates for amphipods in rooms
        for y in range(2, burrow.shape[0] - 1):
            for x in (3, 5, 7, 9):
                find_candidates(
                    burrow, rooms, Pos(y, x), energy,  situations, already_seen)


def find_candidates(burrow, rooms, pos, energy, situations, already_seen):
    amph = burrow[pos]
    if amph in 'ABCD' and not (rooms[amph].pos == pos.x and rooms[amph].is_open(burrow)):
        dests = get_valid_dests(burrow, rooms, pos)
        while not dests.empty():
            num_moves, dest = dests.get()

            new_burrow = burrow.copy()
            new_burrow[dest], new_burrow[pos] = burrow[pos], burrow[dest]

            new_energy = energy + num_moves * rooms[amph].cost
            min_energy = get_min_energy(new_burrow, rooms, new_energy)

            burrow_key = ''.join(new_burrow[1:-1, 1:-1].reshape(-1))
            if burrow_key not in already_seen:
                already_seen.add(burrow_key)
                situations.put(((min_energy, new_energy), new_burrow.tolist()))


def get_valid_dests(burrow, rooms, start):
    amph = burrow[start]
    dests = PriorityQueue()

    current = set([(0, start)])
    while current:
        new_current = set()
        for num_moves, (y, x) in current:
            if y > 1 and x == start.x:
                # get out of room
                if burrow[y - 1, x] != '.':
                    return PriorityQueue()
                new_current.add((num_moves + y - 1, Pos(1, x)))
                current = new_current
                continue
            else:
                if x == rooms[amph].pos and rooms[amph].is_open(burrow):
                    # enter room
                    while burrow[y + 1, x] == '.':
                        y += 1
                        num_moves += 1
                    dests = PriorityQueue()
                    dests.put((num_moves, Pos(y, x)))
                    return dests
                else:
                    # move in hallway
                    if x >= start.x and burrow[y, x + 1] == '.':
                        new_dest = (num_moves + 1, Pos(y, x + 1))
                        new_current.add(new_dest)
                        if start.y > 1 and x + 1 not in (3, 5, 7, 9):
                            dests.put(new_dest)
                    if x <= start.x and burrow[y, x - 1] == '.':
                        new_dest = (num_moves + 1, Pos(y, x - 1))
                        new_current.add(new_dest)
                        if start.y > 1 and x - 1 not in (3, 5, 7, 9):
                            dests.put(new_dest)

        current = new_current

    return dests


def get_min_energy(burrow, rooms, energy):
    room_depths = {}
    for room in rooms.values():
        for depth, amph in reversed(list(enumerate(burrow[2:-1, room.pos]))):
            if amph != room.name:
                room_depths[room.name] = depth + 1
                break

    family_moves = defaultdict(int)
    for room, room_depth in room_depths.copy().items():
        for depth, amph in enumerate(burrow[2:2 + room_depth, rooms[room].pos]):
            if amph != '.':
                family_moves[amph] += depth + 1 + \
                    abs(rooms[room].pos - rooms[amph].pos) + room_depths[amph]
                room_depths[amph] -= 1

    for pos, amph in enumerate(burrow[1, 1:-1]):
        if amph != '.':
            family_moves[amph] += \
                abs(pos - rooms[amph].pos) + room_depths[amph]
            room_depths[amph] -= 1

    min_energy = energy
    for family, min_moves in family_moves.items():
        min_energy += rooms[family].cost * min_moves

    return min_energy


def part1(burrow):
    doors = np.flatnonzero(burrow[2] != '#')
    rooms = {name: Room(name, pos) for name, pos in zip('ABCD', doors)}

    situations = PriorityQueue()
    situations.put(((float('inf'), 0), burrow))
    return find_solution(situations, rooms)


def part2(burrow):
    doors = np.flatnonzero(burrow[2] != '#')
    rooms = {name: Room(name, pos) for name, pos in zip('ABCD', doors)}

    new_data = np.stack([list('  #D#C#B#A#  '), list('  #D#B#A#C#  ')])
    burrow = np.vstack([burrow[:3], new_data, burrow[3:]])

    situations = PriorityQueue()
    situations.put(((float('inf'), 0), burrow))
    return find_solution(situations, rooms)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (12521, 44169),
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
