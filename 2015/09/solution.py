import os
import sys
from collections import defaultdict
from operator import gt, lt


def transform(puzzle):
    routes = defaultdict(set)
    for line in puzzle:
        start, _, end, _, dist = line.split()
        routes[start].add((end, int(dist)))
        routes[end].add((start, int(dist)))

    cities = set(routes.keys())
    for city in cities:
        routes[None].add((city, 0))

    return routes, cities


def travel(routes, to_visit, current, current_dist, current_path, compare):
    best_dist, best_path = None, None

    for city, dist in routes[current]:
        if city not in to_visit:
            continue

        new_dist, new_path = current_dist + dist, current_path + [city]
        dist_traveled, path_taken = travel(
            routes, to_visit - {city}, city, new_dist, new_path, compare)

        if best_dist is None or compare(dist_traveled, best_dist):
            best_dist, best_path = dist_traveled, path_taken

    if best_path is not None:
        return best_dist, best_path

    return current_dist, current_path


def part1(data, compare=lt):
    routes, cities = data
    best_dist, _ = travel(routes, cities, None, 0, [], compare=compare)
    return best_dist


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(compare=gt)

    # solutions to examples given for validation
    test_solutions = [
        (605, 982),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
