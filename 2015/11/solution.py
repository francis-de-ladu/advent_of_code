import os
import sys


def transform(puzzle):
    return list(puzzle[0])


def check_requirements(password, num_pairs):
    # first condition
    char_values = [ord(c) for c in password]
    for v1, v2, v3 in zip(char_values, char_values[1:], char_values[2:]):
        if v1 == v2 - 1 and v1 == v3 - 2:
            break
    else:
        return False

    # third condition
    in_pair, pair_cnt = False, 0
    for v1, v2 in zip(char_values, char_values[1:]):
        if in_pair:
            in_pair = False
        elif v1 == v2:
            pair_cnt += 1
            in_pair = True

    return pair_cnt == num_pairs


def part1(password, forbidden=set(['i', 'o', 'l']), num_pairs=2, num_next=2):
    next_passwords = []
    last_idx = len(password) - 1

    for i in range(num_next):
        idx = last_idx

        got_forbidden = False
        for i, c in enumerate(password):
            if got_forbidden:
                password[i] = 'a'
            elif c in forbidden:
                password[i] = chr(ord(password[i]) + 1)
                got_forbidden = True

        is_valid = False
        while not is_valid:
            # get index of next char to increment
            while password[idx] == 'z':
                idx -= 1

            # second condition
            new_char = password[idx]
            while (new_char := chr(ord(new_char) + 1)) in forbidden:
                pass

            # build new password
            password[idx] = new_char
            for i, _ in enumerate(password[idx + 1:]):
                password[idx + 1 + i] = 'a'
            idx = last_idx

            # check if valid
            is_valid = check_requirements(password, num_pairs)

        next_passwords.append(''.join(password))

    return tuple(next_passwords)


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        ('abcdffaa', None),
        ('ghjaabcc', None),
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
