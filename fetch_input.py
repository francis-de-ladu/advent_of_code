import argparse
import json
import os
from datetime import date

import requests


def _get_cookie(path="cookie.json"):
    with open(path, 'r') as file:
        return json.load(file)


def _fetch_input(day, year):
    output_dir = f"bix{year}-12-{day}"
    output_file = f"{output_dir}/puzzle.txt"
    os.makedirs(f"{output_dir}/tests", exist_ok=True)

    if not os.path.exists(output_file):
        input_url = f"https://adventofcode.com/{year}/day/{day}/input"

        try:
            response = requests.get(url=input_url, cookies=_get_cookie())
            response.raise_for_status()
            puzzle_input = response.text
        except requests.HTTPError:
            exit({"status_code": response.status_code,
                  "details": response.text})

        with open(output_file, 'w') as file:
            file.write(puzzle_input)


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

    _fetch_input(day=args.day, year=args.year)
