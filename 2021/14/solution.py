import os
import sys
from collections import defaultdict
from operator import itemgetter


def transform(puzzle):
    template = puzzle[0]
    rules = map(lambda x: x.split(' -> '), puzzle[2:])
    rules = {pattern: insertion for pattern, insertion in rules}
    return template, rules


def part1(data, num_iters=10):
    # unpack data
    template, rules = data

    # compute counts of the patterns in template
    patterns = defaultdict(int)
    for pattern in map(''.join, zip(template, template[1:])):
        patterns[pattern] += 1

    # for each iteration in num_iters, compute new pattern counts
    for _ in range(num_iters):
        new_patterns = defaultdict(int)
        for pattern, cnt in patterns.items():
            pair1 = pattern[0] + rules[pattern]
            pair2 = rules[pattern] + pattern[1]
            new_patterns[pair1] += cnt
            new_patterns[pair2] += cnt

        # replace old pattern dict with new pattern dict
        patterns = new_patterns

    # compute element counts from pattern counts (will be twice the true count)
    counts = defaultdict(int)
    for pattern, cnt in patterns.items():
        counts[pattern[0]] += cnt
        counts[pattern[1]] += cnt

    # first and last elements of template have only been counted once
    counts[template[0]] += 1
    counts[template[-1]] += 1

    # sort elements by reverse counts, then return most common minus least
    # common divided by 2 since elements have been counted twice
    sorted_elems = sorted(counts.items(), key=itemgetter(1), reverse=True)
    return (sorted_elems[0][1] - sorted_elems[-1][1]) // 2


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(num_iters=40)

    # solutions to examples given for validation
    test_solutions = [
        (1588, 2188189693529),
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
