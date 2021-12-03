import argparse
import os
from datetime import date
from distutils.dir_util import copy_tree

import requests
from utils import _get_cookie


def fetch_input(day, year):
    # output directory and file where to save fetched input
    day_str = f'0{day}' if day < 10 else day
    output_dir = f"{year}/{day_str}"
    output_file = f"{output_dir}/puzzle.txt"

    if not os.path.exists(output_file):
        # url where to get the input
        input_url = f"https://adventofcode.com/{year}/day/{day}/input"

        try:
            # send get request, raise on error
            response = requests.get(url=input_url, cookies=_get_cookie())
            response.raise_for_status()

        except requests.HTTPError:
            # display error and exit
            exit({"status_code": response.status_code,
                  "details": response.text})

        # create day directory from template if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs("template/tests", exist_ok=True)
            copy_tree("template", output_dir)

        # save input puzzle to file
        with open(output_file, 'w') as file:
            file.write(response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch `Advent of Code` puzzle inputs.")

    parser.add_argument(
        '--day', type=int, default=date.today().day,
        help="day of the puzzle to fetch (defaults to current day)")
    parser.add_argument(
        '--year', type=int, default=date.today().year,
        help="year of the puzzle to fetch (defaults to current year)")

    args = parser.parse_args()

    fetch_input(day=args.day, year=args.year)
