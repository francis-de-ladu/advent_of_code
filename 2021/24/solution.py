import os
import sys
from itertools import product, starmap
from operator import add, eq, floordiv, mod, mul

from tqdm import tqdm


def transform(puzzle):
    return puzzle


def exec_instruction(model_no, vars, instr):
    instr, operands = instr[:3], instr[4:]
    # print()
    # print(instr, operands)
    if instr == 'inp':
        vars[operands], model_no = int(model_no[0]), model_no[1:]
    else:
        op1, op2 = operands.split()
        op2 = vars[op2] if op2 in vars else int(op2)
        # print(op1, op2, vars)
        vars[op1] = {
            'ass': lambda a, b: b,
            'add': lambda a, b: a + b,
            'mul': lambda a, b: a * b,
            'div': lambda a, b: a // b,
            'mod': lambda a, b: a % b,
            'eql': lambda a, b: int(a == b),
        }[instr](vars[op1], op2)

    # print(vars)
    return vars, model_no


def eval_operand(vars, operand):
    if operand in vars:
        return vars[operand]
    return {int(operand)}


def part1(data):
    reduced_set = data
    current_op = [data[0]]

    while True:
        vars = {'w': set(map(int, '123456789')), 'x': {0}, 'y': {0}, 'z': {0}}
        print()
        data = reduced_set
        reduced_set = []
        for i, instr1 in enumerate(data[1:]):
            # compare instruction target var with current operation target var
            if not instr1.startswith('inp') and instr1[4] == current_op[0][4] and i != len(data) - 1:
                current_op.append(instr1)
                continue

            if i == len(data) - 1:
                current_op.append(instr1)

            combined = []
            for instr2 in current_op:
                operator, target, operands = \
                    instr2[:3], instr2[4], instr2[4:].split()
                # print(instr2, operator, target, operands)
                operands = [eval_operand(vars, op) for op in operands]

                if operator == 'inp':
                    result = set(map(int, '123456789'))
                else:
                    if operator == 'ass':
                        result = operands[-1]
                    elif operator == 'add':
                        result = set(starmap(add, product(*operands)))
                    elif operator == 'mul':
                        result = set(starmap(mul, product(*operands)))
                    elif operator == 'div':
                        operands[-1].discard(0)
                        result = set(starmap(floordiv, product(*operands)))
                    elif operator == 'mod':
                        operands[-1].discard(0)
                        result = set(starmap(mod, product(*operands)))
                    elif operator == 'eql':
                        result = set(map(int, starmap(eq, product(*operands))))
                    else:
                        print(f'Invalid instruction: {instr2}')
                        exit()

                if result == vars[target] and 'w' not in instr2:
                    continue

                if len(result) == 1:
                    combined = [f'ass {target} {list(result)[0]}']
                elif result == operands[-1]:
                    combined = [f'ass {target} {instr2[6:]}']
                else:
                    combined.append(instr2)

                vars[target] = result

            reduced_set.extend(combined)
            current_op = [instr1]
            print(i, len(reduced_set))

        for i, instr in enumerate(reduced_set):
            print(i + 1, instr)

        if len(reduced_set) == len(data):
            break

    for model_no in tqdm(map(str, range(99999999999999, 0, -1))):
        if '0' in model_no:
            continue

        model_no_backup = model_no

        vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        for i, instr in enumerate(data):
            # print(i, instr)
            try:
                vars, model_no = exec_instruction(model_no, vars, instr)
            except ZeroDivisionError:
                print("ERROR")
                vars['z'] = -1
                break

        print(model_no_backup, vars)
        if vars['z'] == 0:
            return model_no_backup

    return


def part2(data):
    return


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
        part2=part2,
        p1_kwargs=p1_kwargs,
        p2_kwargs=p2_kwargs,
        test_solutions=test_solutions,
        submit=False,
        verbose=False,
    )

    # load puzzle, run tests, attempt submission
    run_everything(**kwargs)
