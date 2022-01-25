import json
import os
import re
import sys
import time
from pathlib import Path

import requests


def timeit(func):
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()

        print(f'func `{func.__name__}` took: {te-ts:2.4f} sec')
        return result

    return timed


def _get_cookie(path="cookie.json"):
    # the content of the cookie file should look like:
    #     {"session": <your_cookie_as_string_here>}
    with open(path, 'r') as file:
        return json.load(file)


def get_puzzle_data(input_path, transform, verbose=False):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    if verbose:
        print("Puzzle:")
        print(puzzle)
        print()

    transformed = transform(puzzle)
    if verbose:
        print("Transformed:")
        print(transformed)
        print()

    return transformed


def run_on_input(input_path, part1, part2, p1_kwargs, p2_kwargs,
                 solution1=None, solution2=None, submit=False, **kwargs):
    # retrieve and transform puzzle data
    data = get_puzzle_data(input_path, **kwargs)

    # execute parts 1 and 2 on the data
    answer1 = part1(data, **p1_kwargs)
    if isinstance(answer1, tuple):
        answer1, answer2 = answer1
    else:
        answer2 = part2(data, **p2_kwargs)

    print(Path(input_path).stem.upper() + ':')
    print("Part1:", answer1)
    print("Part2:", answer2)
    print()

    if answer1 is not None:
        assert solution1 is None or answer1 == solution1, \
            f"got part 1 answer `{answer1}`, but was expeting `{solution1}`"

    if answer1 is not None and answer2 is not None:
        assert solution2 is None or answer2 == solution2, \
            f"got part 2 answer `{answer2}`, but was expeting `{solution2}`"

    if submit is True:
        directory = Path(input_path).parent
        # if you got here, all went well with tests, so submit solution
        year, day = map(int, directory.parts[-2:])
        if answer2 is not None:
            submit_solution(year, day, answer2, part=2)
        elif answer1 is not None:
            submit_solution(year, day, answer1, part=1)
        else:
            print("There was no answer to submit...")


def submit_solution(year, day, answer, part):
    # url where the answer will be sutmitted
    answer_url = f"https://adventofcode.com/{year}/day/{day}/answer"

    # request headers and data
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {'level': part, 'answer': answer}

    try:
        # send post request, raise on error
        session = requests.Session()
        response = session.post(
            answer_url, cookies=_get_cookie(), headers=headers, data=data)
        response.raise_for_status()
        print(response)
    except requests.HTTPError:
        exit({"status_code": response.status_code,
              "details": response.text})


def numerically_sorted(path_entries):
    sorted_entries = sorted(
        path_entries, key=lambda ent: int(re.search(r'\d+', ent.name).group()))
    return [entry.path for entry in sorted_entries]


def run_everything(test_solutions, submit=True, **kwargs):
    # retrieve parent directory of the file lauched from command line
    directory = Path(sys.argv[0]).parent

    # run tests and exit with error if validation fails
    dir_scanner = os.scandir(f"{directory}/tests")
    test_paths = numerically_sorted([entry for entry in dir_scanner])
    for path, (sol1, sol2) in zip(test_paths, test_solutions):
        run_on_input(path, solution1=sol1, solution2=sol2, **kwargs)

    # run with puzzle data
    run_on_input(f"{directory}/puzzle.txt", submit=submit, **kwargs)
