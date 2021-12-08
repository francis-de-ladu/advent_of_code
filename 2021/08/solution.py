import os
import sys


def transform(puzzle):
    return [Entry(entry) for entry in puzzle]


class Entry():
    def __init__(self, entry):
        entry = entry.replace(' | ', ' ')
        patterns = [frozenset(p) for p in entry.split()]
        # simplify future lookups by sorting easy and hard patterns by lengths
        self.easy = sorted(list(filter(is_easy, patterns[:10])), key=len)
        self.hard = sorted(list(filter(is_hard, patterns[:10])), key=len)
        self.output = patterns[10:]


def is_easy(pattern):
    return len(pattern) in {2, 3, 4, 7}


def is_hard(pattern):
    return not is_easy(pattern)


def get_matches(entry, mapping, digit, condition):
    matches = [p for p in entry.to_map if condition(p, mapping[digit])]
    # remove matches from patterns left to map
    entry.to_map = [p for p in entry.to_map if p not in matches]
    return matches


def part1(data):
    easy_digits_cnt = 0
    for entry in data:
        easy_digits_cnt += len(list(filter(is_easy, entry.output)))
    return easy_digits_cnt


def part2(data):
    outputs = []
    for entry in data:
        mapping = dict(zip([1, 7, 4, 8], entry.easy))
        entry.to_map = entry.hard

        mapping[9], = get_matches(entry, mapping, 4, set.issuperset)
        mapping[3], mapping[0] = get_matches(entry, mapping, 7, set.issuperset)

        mapping[5], = get_matches(entry, mapping, 9, set.issubset)
        mapping[6], = get_matches(entry, mapping, 5, set.issuperset)

        mapping[2] = entry.to_map.pop()

        reverse_mapping = {v: k for k, v in mapping.items()}
        output_mapping = (reverse_mapping[o] for o in entry.output)
        outputs.append(int(''.join(map(str, output_mapping))))

    return sum(outputs)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (26, 61229),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
