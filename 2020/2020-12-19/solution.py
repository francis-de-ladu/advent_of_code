import os
import re
import sys
from os.path import abspath, dirname
from pathlib import Path


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read()  # .splitlines()

    puzzle = re.sub(r"\"", "", puzzle)
    rules, messages = puzzle.split('\n\n')

    return rules, messages


def part1(rules, messages):
    # the pattern to find rules that are terminal
    pattern = re.compile(r"(\d+)\:\s([ab\s|()\+\*]+)$", re.MULTILINE)

    subtitution = True
    while subtitution:
        subtitution = False
        for match in re.findall(pattern, rules):
            if match[0] == '0':
                continue
            subtitution = True
            rules = re.sub(r"\b{}\b".format(match[0]), f"({match[1]})", rules)

    # get and format content of rule 0
    rule_0 = [rule.replace(' ', '') for rule in rules.split('\n')
              if rule.startswith("0:")]
    rule_0 = rule_0[0][2:]
    rule_0 = re.sub(r"\((a|b)\)", r"\1", rule_0)

    # filter out messages that don't match the rule
    matches = [message for message in messages.split('\n')
               if re.fullmatch(r"{}".format(rule_0), message)]

    return len(matches)


def part2(rules, messages):
    return


def run_on_input(input_path, solution1=None, solution2=None):
    rules, messages = prepare_input(input_path)

    answer1 = part1(rules, messages)

    # new rule number 8
    rules = rules.replace("8: 42", "8: 42+")

    # new rule number 11 (stopped at 10 repetitions, could fail)
    new_11 = [' '.join(['42'] * i + ['31'] * i) for i in range(1, 10)]
    rules = rules.replace("11: 42 31", f"11: ({' | '.join(new_11)})")

    answer2 = part1(rules, messages)

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

    # test solutions (one tuple per test -> (part1, part2))
    solutions = [(2, None), (2, None), (3, 12)]

    # run test puzzles
    dir_scanner = os.scandir(f"{directory}/tests")
    test_paths = sorted([entry.path for entry in dir_scanner])
    for path, (sol1, sol2) in zip(test_paths, solutions):
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
