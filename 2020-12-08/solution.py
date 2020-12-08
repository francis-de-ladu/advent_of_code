import re

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    instructions = input_file.read().splitlines()


# helper function

def execute(IP, acc, visited, can_change):
    if IP in visited or IP == len(instructions):
        return IP, acc
    visited.add(IP)
    instr, val = instructions[IP].split()
    if instr == 'nop':
        if can_change:
            result = execute(IP + int(val), acc, visited.copy(), False)
            if result[0] == len(instructions):
                return result
        return execute(IP + 1, acc, visited, can_change)
    elif instr == 'jmp':
        if can_change:
            result = execute(IP + 1, acc, visited.copy(), False)
            if result[0] == len(instructions):
                return result
        return execute(IP + int(val), acc, visited, can_change)
    else:
        return execute(IP + 1, acc + int(val), visited, can_change)


# part 1

IP, acc = execute(0, 0, set(), False)
print(acc)


# part 2

IP, acc = execute(0, 0, set(), True)
print(acc)
