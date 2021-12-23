import math
import os
import sys
from copy import deepcopy


class SnailfishNumber():
    def __init__(self, left, right=None, parent=None, depth=0, max_depth=4):
        self.depth, self.max_depth = depth, max_depth
        self.parent = parent

        if right is None:
            self.value = left
            self.left = self.right = None
        else:
            if isinstance(left, int):
                left = [left]
            if isinstance(right, int):
                right = [right]
            if isinstance(left, list):
                left, right = SnailfishNumber(*left), SnailfishNumber(*right)

            self.value = None
            self.left, self.right = left, right
            self.left.parent = self.right.parent = self

    @property
    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __str__(self):
        if isinstance(self.value, int):
            return f'{self.value}'
        return f'[{self.left}, {self.right}]'


def explode_too_nested(node, depth=1, max_depth=4):
    if node.value is not None:
        return False
    elif depth > max_depth:
        explode_left(node, node.left.value)
        explode_right(node, node.right.value)
        node.left = node.right = None
        node.value = 0
        return True

    return explode_too_nested(node.left, depth + 1, max_depth) \
        or explode_too_nested(node.right, depth + 1, max_depth)


def explode_left(node, value):
    while node is node.parent.left:
        node = node.parent
        if not node.parent:
            return
    node = node.parent.left
    while node.right:
        node = node.right
    node.value += value


def explode_right(node, value):
    while node is node.parent.right:
        node = node.parent
        if not node.parent:
            return
    node = node.parent.right
    while node.left:
        node = node.left
    node.value += value


def split_too_high(node, max_value=9):
    if node.value:
        if node.value > max_value:
            value_halved = node.value / 2
            node.left = SnailfishNumber(math.floor(value_halved), parent=node)
            node.right = SnailfishNumber(math.ceil(value_halved), parent=node)
            node.value = None
            return True
        return False

    return node.left and split_too_high(node.left, max_value) \
        or node.right and split_too_high(node.right, max_value)


def transform(puzzle):
    evaluated = map(eval, puzzle)
    normalized = map(lambda n: [n] if isinstance(n, int) else n, evaluated)
    numbers = [SnailfishNumber(*number) for number in normalized]
    return numbers


def part1(numbers):
    numbers = deepcopy(numbers)

    root = numbers.pop(0)
    for number in numbers:
        root = SnailfishNumber(root, number)
        root.left.parent = root.right.parent = root
        while explode_too_nested(root) or split_too_high(root):
            pass

    return root.magnitude


def part2(numbers):
    numbers = deepcopy(numbers)

    best_magnitude = 0
    for i, num1 in enumerate(numbers[:-1]):
        for j, num2 in enumerate(numbers[i + 1:]):
            # first addition
            res1 = SnailfishNumber(deepcopy(num1), deepcopy(num2))
            res1.left.parent = res1.right.parent = res1
            while explode_too_nested(res1) or split_too_high(res1):
                pass
            best_magnitude = max(res1.magnitude, best_magnitude)

            # second addition
            res2 = SnailfishNumber(deepcopy(num2), deepcopy(num1))
            res2.left.parent = res2.right.parent = res2
            while explode_too_nested(res2) or split_too_high(res2):
                pass
            best_magnitude = max(res2.magnitude, best_magnitude)

    return best_magnitude


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (4140, 3993),
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
