import re

import numpy as np


def part1(addresses, values):
    # initialize memory to 0
    memory = np.zeros(max(addresses) + 1, dtype=np.int)

    for addr, val in zip(addresses, values):
        # split chars of the value
        val = np.asarray(list(val))

        if addr < 0:
            mask = val
        else:
            new_val = np.where(mask != 'X', mask, val)
            memory[addr] = int(''.join(new_val), 2)

    return np.sum(memory)


def part2(addresses, values):
    # represent memory as dict to avoid allocating an array of size 2^36
    memory = {}

    for addr, val in zip(addresses, values):
        if addr < 0:
            # split chars of the value
            mask = np.asarray(list(val))
            continue

        # convert address to 36-bit binary representation
        floating_addr = np.asarray(list(format(addr, "036b")))

        # swap address bits where needed to get floating address
        condition = (mask == '1') | (mask == 'X')
        floating_addr = np.where(condition, mask, floating_addr)

        # find floating bit indices
        floating_bits = \
            [i for i, bit in enumerate(floating_addr) if bit == 'X']

        num_floating = len(floating_bits)
        format_str = f"0{num_floating}b"  # to add leading 0s to replacements

        # compute all possible replacements for this number of floating bits
        replacements = \
            [list(format(i, format_str)) for i in range(2**num_floating)]
        replacements = np.asarray(replacements)

        # replace floating bits in the address by those in `replacements`
        to_overwrite = np.vstack([floating_addr] * replacements.shape[0])
        to_overwrite[:, floating_bits] = replacements

        # convert addresses back to base 10, then set value
        to_overwrite = [int(''.join(addr), 2) for addr in to_overwrite]

        # set value into memory addresse to overwrite
        for addr in to_overwrite:
            memory[addr] = int(val, 2)

    return sum(memory.values())


if __name__ == "__main__":
    with open("puzzle.txt", 'r') as input_file:
        puzzle = input_file.read().splitlines()

    addresses, values = zip(*[line.split(' = ') for line in puzzle])

    addresses = [int(re.sub(r"[^\d]", "", addr))
                 if addr != 'mask' else -1 for addr in addresses]
    values = [format(int(val), "036b")
              if val.isnumeric() else val for val in values]

    # print(addresses)
    # print(values)

    print("Part1:", part1(addresses, values))
    print("Part2:", part2(addresses, values))
