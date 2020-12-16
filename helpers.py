import json
import os
from distutils.dir_util import copy_tree

import requests


def _get_cookie(path="cookie.json"):
    with open(path, 'r') as file:
        return json.load(file)


def fetch_input(day, year):
    # output directory and file where to save fetched input
    output_dir = f"{year}-12-{day}"
    output_file = f"{output_dir}/puzzle.txt"

    # create day directory from template if it doesn't exist
    if not os.path.exists(output_dir):
        copy_tree("template", output_dir)

    if not os.path.exists(output_file):
        # url where to get the input
        input_url = f"https://adventofcode.com/{year}/day/{day}/input"

        try:
            # send get request, raise on error
            response = requests.get(url=input_url, cookies=_get_cookie())
            response.raise_for_status()
        except requests.HTTPError:
            exit({"status_code": response.status_code,
                  "details": response.text})

        # save input puzzle to file
        with open(output_file, 'w') as file:
            file.write(response.text)


def submit_solution(year, day, answer, level):
    # parts from which the url will be built
    base_url = f"https://adventofcode.com/{year}/day/{day}/answer?"
    query_params = f"level={level}&answer={answer}"

    # url where the answer will be sutmitted
    answer_url = base_url + query_params

    try:
        # send post request, raise on error
        response = requests.post(url=answer_url, cookies=_get_cookie())
        response.raise_for_status()
    except requests.HTTPError:
        exit({"status_code": response.status_code,
              "details": response.text})
