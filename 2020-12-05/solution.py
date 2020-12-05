import re

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read()  # .splitlines()

puzzle = re.sub(r"[BR]", '1', puzzle)
puzzle = re.sub(r"[FL]", '0', puzzle)
puzzle = puzzle.splitlines()


def bin2dec(bin):
    dec = 0
    for bit in bin:
        dec = 2 * dec + int(bit)
    return dec


# puzzle 1

seats = set(map(bin2dec, puzzle))
print("highest_id:", max(seats))


# puzzle 2

for i in range(1024):
    if i not in seats and i - 1 in seats and i + 1 in seats:
        break

print("my_seat:", i)
