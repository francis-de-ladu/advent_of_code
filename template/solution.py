import os
from pathlib import Path


def run_on_input(input_path):
    _ = prepare_input(input_path)

    print('\n' + Path(input_path).stem.upper() + ':')
    print("Part1:", part1())
    print("Part2:", part2())


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    return puzzle


def part1():
    return


def part2():
    return


if __name__ == "__main__":
    # tests
    for entry in os.scandir("tests"):
        run_on_input(entry.path)

    # puzzle
    run_on_input("puzzle.txt")
    print()
