import os
import sys
from copy import deepcopy
from operator import itemgetter


class Person:
    def __init__(self, hp, damage, armor=0, mana=None):
        self.hp = hp
        self.damage = damage
        self._armor = armor
        self.mana = mana
        self.shield_armor = 0

    @property
    def armor(self):
        return self._armor + self.shield_armor

    def __repr__(self):
        return f'hp={self.hp} mana={self.mana} ' \
            f'damage={self.damage} armor={self.armor}'


def transform(puzzle):
    player = Person(50, 0, 0, mana=500)
    boss = Person(*[int(line.split()[-1]) for line in puzzle])
    return player, boss


def apply_effects(player, boss, active_effects):
    still_active = []
    for (effect, timer) in active_effects:
        if effect == 'poison':
            boss.hp -= 3
        elif effect == 'recharge':
            player.mana += 101
        elif effect == 'shield' and timer == 1:
            player.shield_armor = 0

        if timer > 1:
            still_active.append((effect, timer - 1))

    return player, boss, still_active


def get_cost(spell, costs=dict(missile=53, drain=73, shield=113, poison=173, recharge=229)):
    return costs.get(spell)


def try_spell(spell, characters, active_effects, mana_spent, min_spent, hard_mode):
    player, boss = characters

    # PLAYER'S TURN

    mana_cost = get_cost(spell)
    player.mana -= mana_cost
    mana_spent += mana_cost

    if spell == 'missile':
        boss.hp -= 4
    elif spell == 'drain':
        boss.hp -= 2
        player.hp += 2
    elif spell == 'shield':
        player.shield_armor = 7
        active_effects.append((spell, 6))
    elif spell == 'poison':
        active_effects.append((spell, 6))
    elif spell == 'recharge':
        active_effects.append((spell, 5))

    # check if boss is dead
    if boss.hp <= 0 or mana_spent >= min_spent:
        return min(min_spent, mana_spent)

    # BOSS'S TURN

    *characters, active_effects = apply_effects(*characters, active_effects)

    # check if player is dead
    player.hp -= max(1, boss.damage - player.armor)
    player.hp -= bool(hard_mode)
    if player.hp <= 0:
        return min_spent

    # play next round
    return play_round(characters, active_effects, mana_spent, min_spent, hard_mode)


def play_round(characters, active_effects, mana_spent, min_spent, hard_mode):
    player, _ = characters
    *characters, active_effects = apply_effects(*characters, active_effects)

    # get spells, than remove those that are already active
    spells = set(['missile', 'drain', 'shield', 'poison', 'recharge'])
    spells -= set(map(itemgetter(0), active_effects))

    # remove spells with cost higher than remaining mana
    spells = set([spell for spell in spells if get_cost(spell) <= player.mana])
    if len(spells) == 0:
        return min_spent

    # attempt every spell
    for spell in spells:
        min_spent = try_spell(
            spell, deepcopy(characters), deepcopy(active_effects), mana_spent, min_spent, hard_mode)

    return min_spent


def part1(characters, hard_mode=False):
    player, _ = characters
    if hard_mode:
        player.hp -= 1

    min_mana_spent = play_round(
        deepcopy(characters), [], 0, float('inf'), hard_mode)

    return min_mana_spent


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(hard_mode=True)

    # solutions to examples given for validation
    test_solutions = [
        (False, False),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=True,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
