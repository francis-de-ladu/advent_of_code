import os
import sys


def transform(puzzle):
    return puzzle


def get_int_value(data, block_len, instr_idx):
    indices = range(instr_idx, len(data), block_len)
    return [int(data[idx].split()[-1]) for idx in indices]


def part1(data, block_len=18, inc_x_idx=5, inc_y_idx=15, div_z_idx=4, inp_w_values=range(9, 0, -1)):
    inc_x = get_int_value(data, block_len, inc_x_idx)
    # inc_y = get_int_value(data, block_len, inc_y_idx)
    # div_z = get_int_value(data, block_len, div_z_idx)

    vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    xs = [int(not any(x + inc in range(1, 10) for x in range(26)))
          for inc in inc_x]

    model_no = search_best_input(
        data, vars.copy(), '', xs, block_len, inp_w_values)

    return int(model_no)


def search_best_input(instrs, vars, prefix, xs, block_len, inp_w_values):
    if len(instrs) == 0:
        return prefix

    for inp_w in map(str, inp_w_values):
        try:
            block, rest = instrs[:block_len], instrs[block_len:]
            new_vars = run_on_block(
                inp_w, vars.copy(), xs[0], block)
            model_no = search_best_input(
                rest, new_vars.copy(), prefix + inp_w, xs[1:], block_len, inp_w_values)
            if model_no is not None:
                return model_no
        except Exception:
            pass

    return None


def run_on_block(model_no, vars, x_val, instrs):
    for i, instr in enumerate(instrs):
        vars, model_no = exec_instruction(model_no, vars, instr)
        if instr == 'eql x 0' and vars['x'] != x_val:
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
    p2_kwargs = dict(inp_w_values=range(1, 10))

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
