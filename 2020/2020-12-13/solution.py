import numpy as np


def modular_inverse(base, mod):
    for i in range(mod):
        if base * i % mod == 1:
            return i
    else:
        raise ValueError(
            f"(mod {mod}) modular inverse doesn't exist for value {base}")


def part1(timestamp, buses):
    next_departures = [bus - (timestamp % bus) for bus in buses]
    soonest_index = np.argmin(next_departures)
    return buses[soonest_index] * next_departures[soonest_index]


def part2(timestamp, indices, buses):
    modulos = np.asarray(buses)
    remainders = np.asarray([bus - idx for idx, bus in zip(indices, buses)])

    mod_product = np.prod(modulos)
    ys = mod_product // modulos

    zs = np.asarray([modular_inverse(y, mod) for y, mod in zip(ys, modulos)])

    x = np.sum(remainders * ys * zs)
    return x % mod_product


if __name__ == "__main__":
    with open("puzzle.txt", 'r') as input_file:
        puzzle = input_file.read().splitlines()

    timestamp = int(puzzle[0])

    indexed_buses = \
        [(i, int(bus)) for i, bus in enumerate(puzzle[1].split(','))
         if bus != 'x']

    indices, buses = zip(*indexed_buses)

    print("Part1:", part1(timestamp, buses))
    print("Part2:", part2(timestamp, indices, buses))
