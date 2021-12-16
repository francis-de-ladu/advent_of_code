import math
import os
import sys
from operator import eq, gt, lt


def bin2dec(bin_str):
    return int(bin_str, base=2)


class Packet():
    def __init__(self, data, TYPE_LITERAL=4, GROUP_SIZE=5, BITS_M0=15, BITS_M1=11):
        self._value = None
        self.subpackets = []

        content = self.parse_header_get_content(data)
        self.remaining = self.parse_content(
            content, TYPE_LITERAL, GROUP_SIZE, BITS_M0, BITS_M1)

    @property
    def value(self):
        if self.type_id == 4:
            return self._value

        operator = (sum, math.prod, min, max, None, gt, lt, eq)[self.type_id]
        if self.type_id >= 5:
            self.subpackets = self.subpackets[:2]

        values = (subpacket.value for subpacket in self.subpackets)
        values = [values] if self.type_id < 5 else values
        return int(operator(*values))

    def parse_header_get_content(self, data):
        self.version, self.type_id = map(bin2dec, (data[:3], data[3:6]))
        return data[6:]

    def parse_content(self, data, TYPE_LITERAL, GROUP_SIZE, BITS_M0, BITS_M1):
        if self.type_id == TYPE_LITERAL:
            self._value, remaining = self.parse_literal(data, GROUP_SIZE)
        else:
            remaining = self.parse_operator(data, BITS_M0, BITS_M1)

        return remaining

    def parse_literal(self, data, GROUP_SIZE):
        groups = []
        while True:
            prefix, value, data = data[0], data[1:GROUP_SIZE], data[GROUP_SIZE:]
            groups.append(value)
            if prefix == '0':
                break

        return bin2dec(''.join(groups)), data

    def parse_operator(self, data, BITS_M0, BITS_M1):
        mode, content = data[0], data[1:]

        if mode == '0':
            subpckts_len, rest = bin2dec(content[:BITS_M0]), content[BITS_M0:]
            subpckts_data, rest = rest[:subpckts_len], rest[subpckts_len:]
            while not all(map(lambda b: b == '0', subpckts_data)):
                subpacket = Packet(subpckts_data)
                subpckts_data = subpacket.remaining
                self.subpackets.append(subpacket)
        else:
            num_subpckts, rest = bin2dec(content[:BITS_M1]), content[BITS_M1:]
            for _ in range(num_subpckts):
                subpacket = Packet(rest)
                rest = subpacket.remaining
                self.subpackets.append(subpacket)

        return rest

    def sum_version_numbers(self):
        running_sum = self.version
        for subpacket in self.subpackets:
            running_sum += subpacket.sum_version_numbers()
        return running_sum


def transform(puzzle):
    hexa = puzzle[0]
    binary = f'{int(hexa, base=16):b}'
    return binary.zfill(4 * len(hexa))


def parse_data(data):
    packet = Packet(data)
    assert all(map(lambda b: b == '0', packet.remaining))
    return packet


def part1(data):
    packet = parse_data(data)
    return packet.sum_version_numbers()


def part2(data):
    packet = parse_data(data)
    return packet.value


if __name__ == "__main__":
    # add grandparent directory to path to allow importing `run_everything`
    sys.path.insert(1, os.path.join(sys.path[0], '../..'))
    from utils import run_everything

    # keyword arguments to part1 and part2 functions
    p1_kwargs = dict()
    p2_kwargs = dict()

    # solutions to examples given for validation
    test_solutions = [
        (16, None),
        (12, None),
        (23, None),
        (31, None),
        (None, 3),
        (None, 54),
        (None, 7),
        (None, 9),
        (None, 1),
        (None, 0),
        (None, 0),
        (None, 1),
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
    run_everything(submit=True, **kwargs)
