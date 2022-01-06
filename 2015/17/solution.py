import os
import sys


def transform(puzzle):
    return sorted(map(int, puzzle), reverse=True)


def get_combinations(containers, num_liters, acc=[]):
    if num_liters == 0:
        return [acc]
    elif not containers or containers[-1] > num_liters:
        return 0

    combinations = []
    for i, current in enumerate(containers):
        others = containers[i + 1:]
        new_combinations = get_combinations(
            others, num_liters - current, acc + [current])
        if new_combinations:
            combinations.extend(new_combinations)

    return combinations


def part1(containers, num_liters=150):
    return len(get_combinations(containers, num_liters))


def part2(containers, num_liters=150):
    combinations = get_combinations(containers, num_liters)
    num_containers = [len(comb) for comb in combinations]
    return len([num for num in num_containers if num == min(num_containers)])


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        # (4, 3),
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
