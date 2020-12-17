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
