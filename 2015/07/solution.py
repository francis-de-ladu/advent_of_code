import os
import sys


def transform(puzzle):
    return puzzle


def get_val(translated, var):
    if var.isnumeric():
        return int(var)
    return translated.get(var, None)


def part1(data, b_override=False):
    to_translate = set(data)
    translated = dict()

    changed = True
    while changed:
        changed = False
        for line in to_translate.copy():
            # split into parts (values, vars, operators)
            parts = line.split()

            if b_override is not False and parts[-1] == 'b':
                var, res = 'b', b_override
            elif len(parts) == 3:
                v1, _, var = parts
                res = get_val(translated, v1)
            elif len(parts) == 4:
                _, v1, _, var = parts
                value = get_val(translated, v1)
                res = ~value if value is not None else None
            else:
                v1, instr, v2, _, var = parts
                val1, val2 = get_val(translated, v1), get_val(translated, v2)
                if val1 is None or val2 is None:
                    continue

                if instr == 'AND':
                    res = val1 & val2
                elif instr == 'OR':
                    res = val1 | val2
                elif instr == 'LSHIFT':
                    res = val1 << val2
                elif instr == 'RSHIFT':
                    res = val1 >> val2

            if res is not None:
                translated[var] = res & 65535
                to_translate.remove(line)
                changed = True

    return translated.get('a', None)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(b_override=46065)

    # solutions to examples given for validation
    test_solutions = [
        (None, None),
    ]

    # keyword arguments of the `run_everything` function
    kwargs = dict(
        transform=transform,
        part1=part1,
        part2=part1,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        verbose=False
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
