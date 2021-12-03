import re

# load and preprocess puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

entries = [re.split(r"(?:-|\s|:\s)", entry) for entry in puzzle]


def numeric2int(entry):
    first_int = int(entry[0])
    second_int = int(entry[1])
    return [first_int, second_int, entry[2], entry[3]]


entries = list(map(numeric2int, entries))
# print(entries)


# puzzle 1

num_valid = 0
for min_cnt, max_cnt, letter, password in entries:
    letter_cnt = password.count(letter)
    if letter_cnt >= int(min_cnt) and letter_cnt <= int(max_cnt):
        num_valid += 1

print(num_valid)


# puzzle 2

num_valid = 0
for pos1, pos2, letter, password in entries:
    if (password[pos1 - 1] == letter) ^ (password[pos2 - 1] == letter):
        num_valid += 1

print(num_valid)
