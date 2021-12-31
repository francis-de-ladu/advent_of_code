import os
import sys
from itertools import product, starmap
from operator import add, eq, floordiv, mod, mul

from tqdm import tqdm


def transform(puzzle):
    return puzzle


def execute_instr(vars, operator, operands):
    # evaluate operands to get their possible values
    operands = [eval_operand(vars, op) for op in operands]

    if operator == 'inp':
        result = set(map(int, '123456789'))
    else:
        a, b = operands
        if operator == 'ass':
            result = b
        elif operator == 'add':
            result = set(starmap(add, product(a, b)))
        elif operator == 'mul':
            result = set(starmap(mul, product(a, b)))
        elif operator == 'div':
            b.discard(0)
            result = set(starmap(floordiv, product(a, b)))
        elif operator == 'mod':
            a = set([val for val in a if val >= 0])
            b = set([val for val in b if val > 0])
            result = set(starmap(mod, product(a, b)))
        elif operator == 'eql':
            result = set(map(int, starmap(eq, product(a, b))))
        else:
            print(f'Invalid operator: {operator}')
            exit()

    return result


def eval_operand(vars, operand):
    # return vars[operand] if operand in vars else {int(operand)}
    if operand.startswith('-') or operand.isnumeric():
        return {int(operand)}

    while isinstance(operand, str):
        operand = vars[operand]

    return operand


def print_instrs(instrs):
    return
    print()
    for i, instr in enumerate(instrs):
        print(i + 1, '-', instr)


def print_instrs2(instrs):
    print()
    for i, instr in enumerate(instrs):
        print(i + 1, '-', instr)


def first_pass(data):
    vars = {'w': set(map(int, '123456789')), 'x': {0}, 'y': {0}, 'z': {0}}
    reduced_set = []

    for i, instr in tqdm(enumerate(data), desc='first_pass', total=len(data)):
        if instr == 'inp w':
            reduced_set.append(instr)
            continue

        operator, *operands = instr.split()
        target = operands[0]

        result = execute_instr(vars, operator, operands)
        if vars[target] != result:
            vars[target] = result
            if len(result) == 1:
                instr = f'ass {target} {list(result)[0]}'
            reduced_set.append(instr)

        # print(i + 1, len(reduced_set))

    print_instrs(reduced_set)
    return reduced_set


def second_pass(data):
    reduced_set, data = data, []

    while len(reduced_set) != len(data):
        vars = {'w': set(map(int, '123456789')), 'x': {0}, 'y': {0}, 'z': {0}}
        data, reduced_set = reduced_set, []

        current_bloc = [data[0]]
        for i, (instr1, instr2) in tqdm(enumerate(zip(data[:-1], data[1:])), desc='second_pass', total=len(data)):
            # compare targets of both instructions
            if instr1[4] == instr2[4]:
                current_bloc.append(instr2)
                continue

            # merge instructions and append result to reduced set
            reduced = reduce_bloc(vars, current_bloc)
            reduced_set.extend(reduced)
            # print(i + 1, len(reduced_set))

            # start next bloc
            current_bloc = [instr2]

        # merge instructions and append result to reduced set
        reduced = reduce_bloc(vars, current_bloc)
        reduced_set.extend(reduced)
        # print(i + 2, len(reduced_set))

        print_instrs(reduced_set)

    return reduced_set


def reduce_bloc(vars, instrs):
    combined = []
    for instr in instrs:
        operator, *operands = instr.split()
        target = operands[0]

        result = execute_instr(vars, operator, operands)
        if result != vars[target]:
            vars[target] = result

        b = operands[-1]
        # if operator != 'inp' and b in vars and result == vars[b]:

        if len(result) == 1:
            combined = [f'ass {target} {list(result)[0]}']
        elif operator != 'inp' and b in vars and result == vars[b]:
            # can be optimized, then we should reorder
            combined = [
                f'ass {target} {b if len(vars[b]) > 1 else list(result)[0]}']
        else:
            combined.append(instr)

    return combined


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


def find_solution(data):
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


def part1(data):
    reduced_set, data = data, []
    while len(reduced_set) != len(data):
        data, reduced_set = reduced_set, []
        reduced_set = first_pass(data)
        reduced_set = second_pass(reduced_set)

    print_instrs2(reduced_set)
    return find_solution(reduced_set)


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
