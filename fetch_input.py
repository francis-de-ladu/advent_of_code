import argparse
from datetime import date

from helpers import fetch_input

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
