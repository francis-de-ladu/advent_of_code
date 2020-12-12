from itertools import product

import numpy as np

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

waiting_area = np.asarray([list(row) for row in puzzle])

original_shape = waiting_area.shape

waiting_area = np.hstack([
    np.full((waiting_area.shape[0], 1), '.'),
    waiting_area,
    np.full((waiting_area.shape[0], 1), '.')
])

waiting_area = np.vstack([
    np.full(waiting_area.shape[1], '.'),
    waiting_area,
    np.full(waiting_area.shape[1], '.')
])

all_false = np.full(original_shape, False)


# part 1

while True:
    occupied_adjacents = np.zeros(original_shape)

    for dx, dy in product([0, 1, 2], repeat=2):
        if dx == 1 and dy == 1:
            continue

        occupied_adjacents += \
            (waiting_area[dx:((dx - 2) or None), dy:((dy - 2) or None)] == '#')

    to_fill = np.where(waiting_area[1:-1, 1:-1] == 'L',
                       occupied_adjacents == 0, all_false)
    to_free = np.where(waiting_area[1:-1, 1:-1] == '#',
                       occupied_adjacents >= 4, all_false)

    if np.all(to_fill == to_free):
        break

    waiting_area[1:-1, 1:-1][to_fill] = '#'
    waiting_area[1:-1, 1:-1][to_free] = 'L'

print(np.sum(waiting_area == '#'))


# part 2


with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

waiting_area = np.asarray([list(row) for row in puzzle])


def is_valid_pos(position, waiting_area):
    return np.all(position >= 0) and np.all(position < waiting_area.shape)


new_state = None

while new_state is None or np.any(new_state != waiting_area):
    if new_state is None:
        new_state = waiting_area.copy()

    waiting_area = new_state.copy()

    shape_x, shape_y = waiting_area.shape
    for i, j in product(range(shape_x), range(shape_y)):
        if waiting_area[i, j] == '.':
            continue

        position = np.asarray([i, j])

        num_occupied = 0
        for dx, dy in product([-1, 0, 1], repeat=2):
            if dx == 0 and dy == 0:
                continue

            direction = np.asarray([dx, dy])
            for distance in range(1, int(1e10)):
                looked_at = position + distance * direction
                if not is_valid_pos(looked_at, waiting_area):
                    break

                looked_at_state = waiting_area[looked_at[0], looked_at[1]]

                if looked_at_state == 'L':
                    break

                if looked_at_state == '#':
                    num_occupied += 1
                    if waiting_area[i, j] == '#' and num_occupied >= 5:
                        new_state[i, j] = 'L'
                    break

        if waiting_area[i, j] == 'L' and num_occupied == 0:
            new_state[i, j] = '#'

print(np.sum(waiting_area == '#'))
