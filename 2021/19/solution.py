import os
import random
import sys
from copy import deepcopy

import numpy as np


def transform(puzzle):
    scanners = []
    for scanner in '\n'.join(puzzle).split('\n\n'):
        beacons = np.asarray([[int(val) for val in line.split(',')]
                              for line in scanner.split('\n')[1:]])
        scanners.append(beacons)

    return scanners


def find_best_candidate(current, scanners, threshold=30):
    best_idx, best_scanner, best_recenter = None, None, None
    current_set = set(np.abs(current).flatten())

    best_overlap = 0
    for i, scanner in enumerate(scanners):
        for coords in scanner:
            # recenter scanner view on beacon located at `coords`
            recentered = scanner - coords

            scanner_set = set(np.abs(recentered).flatten())
            overlap = len(current_set.intersection(scanner_set))
            if overlap > threshold and overlap > best_overlap:
                best_idx, best_overlap = i, overlap
                best_scanner = recentered
                best_recenter = -coords  # to keep original scanner position

    return best_idx, best_scanner, best_recenter


def attempt_merge(current, candidate, recenter, positions, min_overlap=12):
    current_coords, candidate_coords = [], []
    for cur_coords in current:
        for cand_coords in candidate:
            # use absolute values to perform comparisons
            if np.all(np.abs(cur_coords) == np.abs(cand_coords)):
                current_coords.append(cur_coords)
                candidate_coords.append(cand_coords)

    # make sure the overlap is at least the minimum allowed overlap
    if len(current_coords) < min_overlap:
        return current, positions, False

    # for each axis, check the number of equal values
    current_coords = np.asarray(current_coords)
    candidate_coords = np.asarray(candidate_coords)
    comparison = np.sum(current_coords == candidate_coords, axis=0)

    for axis, comp in enumerate(comparison):
        # transform if number of equal values in axis is less than overlap size
        if comp < len(current_coords):
            candidate[:, axis] *= -1
            recenter[axis] *= -1

    # merge scanner with the others
    new_current = np.concatenate([current, candidate], axis=0)
    new_current = np.unique(new_current, axis=0)

    # add newly merged scanner position to the list of scanner positions
    positions = np.append(positions, [recenter], axis=0)

    return new_current, positions, True


def part1(scanners, part2=False):
    scanners = deepcopy(scanners)
    current = scanners.pop(0)
    positions = np.asarray([[0, 0, 0]])

    while scanners:
        # change orientation
        current = np.roll(current, 1, axis=1)
        positions = np.roll(positions, 1, axis=1)
        if random.random() > 0.33:
            current = np.flip(current, axis=1)
            positions = np.flip(positions, axis=1)

        # recenter on another beacon
        new_center_idx = int(random.random() * len(current))
        positions -= current[new_center_idx]
        current -= current[new_center_idx]

        # find best candidate
        idx, scanner, recenter = find_best_candidate(current, scanners)

        if idx is not None:
            # attempt merging candidate with other merged scanners
            current, positions, is_success = \
                attempt_merge(current, scanner, recenter, positions)
            if is_success:
                scanners.pop(idx)

    if part2:
        highest_dist = 0
        for i, pos1 in enumerate(positions):
            for pos2 in positions[i + 1:]:
                highest_dist = max(highest_dist, np.sum(np.abs(pos1 - pos2)))
        return highest_dist

    return len(current)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(part2=True)

    # solutions to examples given for validation
    test_solutions = [
        (79, 3621),
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
