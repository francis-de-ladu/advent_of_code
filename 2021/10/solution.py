import os
import sys


def transform(puzzle):
    return puzzle


def validate(line):
    matching = {')': '(', ']': '[', '}': '{', '>': '<'}

    stack = []
    for c in line:
        if c in {'[', '(', '{', '<'}:
            stack.append(c)
        elif stack[-1] == matching[c]:
            stack.pop()
        else:
            return [stack, c]

    return stack, None


def complete(stack, mult=5):
    scores = {'(': 1, '[': 2, '{': 3, '<': 4}

    cost = 0
    while len(stack):
        cost = mult * cost + scores.get(stack.pop())

    return cost


def part1(data):
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    syntax_errors = map(lambda line: validate(line)[1], data)
    error_scores = map(lambda error: scores.get(error, 0), syntax_errors)
    return sum(list(error_scores))


def part2(data):
    incomplete = []
    for line in data:
        stack, error = validate(line)
        if error is None:
            incomplete.append(stack)

    compl_costs = [complete(line) for line in incomplete]
    return sorted(compl_costs)[len(compl_costs) // 2]


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (26397, 288957),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
