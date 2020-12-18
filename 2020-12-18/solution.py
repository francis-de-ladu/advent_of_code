import operator
import os
import re
import sys
from os.path import abspath, dirname
from pathlib import Path


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    expressions = [re.split(r"(?:\s|(?<=\()|(?=\)))", expr)
                   for expr in puzzle]

    return expressions


class Operator(object):
    def __init__(self, token):
        self.token = token

    def apply(self, x, y):
        if self.token == '+':
            return operator.add(x, y)
        elif self.token == '*':
            return operator.mul(x, y)
        else:
            raise ValueError(f"Unexpected operator -> `{self.token}`")


class Expression(object):
    def __init__(self, expr, precedence):
        self.precedence = precedence
        self.ast = self.parse(expr)

    def parse(self, expr):
        output = []
        stack = []
        for tok in expr:
            if tok.isnumeric():
                output.append(int(tok))
            elif tok in ('+', '*'):
                if len(stack) == 0:
                    stack.append(tok)
                elif self.precedence[tok] > self.precedence[stack[-1]]:
                    stack.append(tok)
                else:
                    while len(stack):
                        if self.precedence[tok] <= self.precedence[stack[-1]]:
                            output.append(stack.pop())
                        else:
                            break
                    stack.append(tok)
            elif tok == '(':
                stack.append(tok)
            elif tok == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()

        while len(stack):
            output.append(stack.pop())

        return output[::-1]

    def evaluate(self):
        stack = []
        while len(self.ast):
            tok = self.ast.pop()
            if isinstance(tok, int):
                stack.append(tok)
            else:
                x = stack.pop()
                y = stack.pop()
                op = Operator(tok)
                stack.append(op.apply(x, y))
        return stack[0]


def part1(expressions, precedence):
    results = [Expression(expr, precedence).evaluate() for expr in expressions]
    return sum(results)


def part2():
    return


def run_on_input(input_path, solution1=None, solution2=None):
    expressions = prepare_input(input_path)

    answer1 = part1(expressions, precedence={'(': 1, ')': 1, '+': 2, '*': 2})
    answer2 = part1(expressions, precedence={'(': 1, ')': 1, '+': 3, '*': 2})

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

    # test solutions
    solutions1 = [71, 51, 26, 437, 12240, 13632]
    solutions2 = [231, 51, 46, 1445, 669060, 23340]

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    test_paths = sorted([entry.path for entry in dir_scanner])
    for path, sol1, sol2 in zip(test_paths, solutions1, solutions2):
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
