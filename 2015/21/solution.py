import os
import re
import sys
from copy import deepcopy
from itertools import chain, combinations, product


class Person:
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def __repr__(self):
        return f'hp={self.hp} damage={self.damage} armor={self.armor}'


class Item:
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = int(cost)
        self.damage = int(damage)
        self.armor = int(armor)

    def __repr__(self):
        return f'[{self.name}] cost={self.cost} ' \
            f'damage={self.damage} armor={self.armor}'


def transform(puzzle):
    player = Person(100, 0, 0)
    boss = Person(*[int(line.split()[-1]) for line in puzzle])
    shop_items = read_shop_data()
    return player, boss, shop_items


def read_shop_data():
    shop_menu = """
        Weapons:    Cost  Damage  Armor
        Dagger        8     4       0
        Shortsword   10     5       0
        Warhammer    25     6       0
        Longsword    40     7       0
        Greataxe     74     8       0

        Armor:      Cost  Damage  Armor
        Leather      13     0       1
        Chainmail    31     0       2
        Splintmail   53     0       3
        Bandedmail   75     0       4
        Platemail   102     0       5

        Rings:      Cost  Damage  Armor
        Damage +1    25     1       0
        Damage +2    50     2       0
        Damage +3   100     3       0
        Defense +1   20     0       1
        Defense +2   40     0       2
        Defense +3   80     0       3
    """

    shop_items = dict()
    category = None
    for line in map(str.strip, shop_menu.splitlines()):
        if not line:
            continue

        if ':' in line:
            category = line.split(':')[0].lower()
            shop_items[category] = []
        else:
            shop_items[category].append(Item(*re.split(r'\s{2,}', line)))

    return shop_items


def valid_combinations(category, shop_items, valid_cnts):
    item_combinations = []
    for cnt in valid_cnts:
        for cat_items in combinations(shop_items[category], r=cnt):
            item_combinations.append(cat_items)

    return item_combinations


def is_winning(player, boss, selected_items):
    player.damage += sum([item.damage for item in selected_items])
    player.armor += sum([item.armor for item in selected_items])

    turn = 0
    characters = [player, boss]
    while player.hp > 0 and boss.hp > 0:
        current, other = characters[turn % 2], characters[(turn + 1) % 2]
        other.hp -= max(1, current.damage - other.armor)
        turn += 1

    return player.hp > 0


def part1(data):
    player, boss, shop_items = data
    weapons = valid_combinations('weapons', shop_items, range(1, 2))
    armors = valid_combinations('armor', shop_items, range(2))
    rings = valid_combinations('rings', shop_items, range(3))

    min_win_cost = float('inf')
    max_loss_cost = 0
    for selected_items in product(weapons, armors, rings):
        selected_items = list(chain(*selected_items))

        cost = sum([item.cost for item in selected_items])
        if cost >= min_win_cost and cost <= max_loss_cost:
            continue

        if is_winning(deepcopy(player), deepcopy(boss), selected_items):
            min_win_cost = min(cost, min_win_cost)
        else:
            max_loss_cost = max(cost, max_loss_cost)

    return min_win_cost, max_loss_cost


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (False, False),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=None,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
