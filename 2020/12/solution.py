import re

import numpy as np

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

instructions = [(line[0], int(line[1:])) for line in puzzle]
# print(instructions)


# helpers

def navigate(instr, coords, direction=None, ferry=None):
    action, value = instr
    if direction is None:
        if action == 'L':
            action, radians = 'ROTATE', np.radians(value)
        elif action == 'R':
            action, radians = 'ROTATE', -np.radians(value)
        elif action == 'F':
            action = 'WAYPOINT'

    if action == 'N':
        coords[1] += value
    elif action == 'S':
        coords[1] -= value
    elif action == 'E':
        coords[0] += value
    elif action == 'W':
        coords[0] -= value
    elif action == 'L':
        direction += np.radians(value)
    elif action == 'R':
        direction -= np.radians(value)
    elif action == 'F':
        coords[0] += value * int(np.cos(direction))
        coords[1] += value * int(np.sin(direction))
    elif action == 'ROTATE':
        rotation_matrix = np.asarray([
            [np.cos(radians), -np.sin(radians)],
            [np.sin(radians), np.cos(radians)],
        ]).astype(int)
        coords = rotation_matrix.dot(coords)
    elif action == 'WAYPOINT':
        ferry += value * coords

    return coords, direction, ferry


# part 1

position = [0, 0]
direction = 0

for instr in instructions:
    position, direction, _ = navigate(instr, position, direction=direction)

print(position, int(np.degrees(direction)) % 360)
print(np.sum(np.abs(position)))


# part 2

waypoint = np.asarray([10, 1])
position = np.asarray([0, 0])

for instr in instructions:
    waypoint, _, position = navigate(instr, waypoint, ferry=position)

print(position, int(np.degrees(direction)) % 360)
print(np.sum(np.abs(position)))
