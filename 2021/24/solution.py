import os
import sys


def transform(puzzle):
    blocks = []
    current = [puzzle[0]]

    for instr in puzzle[1:]:
        if instr == current[0]:
            blocks.append(current)
            current = [instr]
        else:
            current.append(instr)

    blocks.append(current)
    return blocks


def part1(blocks, inc_x_idx=5, inc_y_idx=15, div_z_idx=4, inp_w_vals=range(9, 0, -1)):
    inc_x = [int(block[inc_x_idx].split()[-1]) for block in blocks]
    # inc_y = [int(block[inc_y_idx].split()[-1]) for block in blocks]
    # div_z = [int(block[div_z_idx].split()[-1]) for block in blocks]

    mod_x = 26
    x_eql_w = [1 - mod_x <= inc <= 0 for inc in inc_x]

    vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    model_no = search_best_input(
        blocks, vars.copy(), '', x_eql_w, inp_w_vals)

    return int(model_no)


def search_best_input(blocks, vars, prefix, x_eql_w, inp_w_vals):
    if len(blocks) == 0:
        return prefix

    current, others = blocks[0], blocks[1:]
    for inp_w in map(str, inp_w_vals):
        try:
            new_vars = run_on_block(
                inp_w, vars.copy(), x_eql_w[0], current)
            new_prefix = prefix + inp_w
            new_model_no = search_best_input(
                others, new_vars.copy(), new_prefix, x_eql_w[1:], inp_w_vals)

            if new_model_no is not None:
                return new_model_no

        except Exception:
            pass

    return None


def run_on_block(model_no, vars, x_val, instrs):
    for i, instr in enumerate(instrs):
        vars, model_no = exec_instruction(model_no, vars, instr)
        if instr == 'eql x w' and vars['x'] != x_val:
            raise ValueError()

    return vars


def exec_instruction(model_no, vars, instr):
    op, *operands = instr.split()
    if op == 'inp':
        a, *_ = operands
        vars[a], model_no = int(model_no[0]), model_no[1:]
    else:
        a, b = operands
        b = vars[b] if b in vars else int(b)

        if op == 'div' and b == 0 or op == 'mod' and (vars[a] < 0 or b <= 0):
            raise ZeroDivisionError()

        vars[a] = {
            'add': lambda a, b: a + b,
            'mul': lambda a, b: a * b,
            'div': lambda a, b: a // b,
            'mod': lambda a, b: a % b,
            'eql': lambda a, b: int(a == b),
        }[op](vars[a], b)

    return vars, model_no


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict(inp_w_vals=range(1, 10))

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
