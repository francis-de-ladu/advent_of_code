import os
import sys
from os.path import abspath, dirname
from pathlib import Path


def prepare_input(input_path):
    with open(input_path, 'r') as file:
        puzzle = file.read().splitlines()

    foods = [tuple(line[:-1].split(' (contains ')) for line in puzzle]
    foods = [(set(food[0].split(' ')), food[1].split(', ')) for food in foods]

    return foods


def part1(foods):
    mapping = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen in mapping:
                mapping[allergen] = mapping[allergen].intersection(ingredients)
            else:
                mapping[allergen] = ingredients

    all_ingredients = [ingredient for ingredients, _ in foods
                       for ingredient in ingredients]

    maybe_allergens = set.union(*mapping.values())
    not_allergens = set(all_ingredients).difference(maybe_allergens)

    not_allergens_cnts = \
        [all_ingredients.count(ingredient) for ingredient in not_allergens]

    return sum(not_allergens_cnts), mapping


def part2(mapping):
    true_mapping = {}
    mapped_ingredients = set()
    while len(mapping) > 0:
        for allergen, ingredients in list(mapping.items()):
            candidates = ingredients.difference(mapped_ingredients)
            if len(candidates) == 1:
                ingredient = list(candidates)[0]
                true_mapping[allergen] = ingredient
                mapped_ingredients.add(ingredient)
                del mapping[allergen]

    return ','.join([true_mapping[key] for key in sorted(true_mapping)])


def run_on_input(input_path, solution1=None, solution2=None):
    foods = prepare_input(input_path)

    answer1, mapping = part1(foods)
    answer2 = part2(mapping)

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
    solutions = [(5, "mxmxvkd,sqjhc,fvjkl")]

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
