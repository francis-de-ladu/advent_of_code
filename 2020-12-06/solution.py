# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read()  # .splitlines()

entries = [entry.split('\n') for entry in puzzle[:-1].split('\n\n')]

# part 1

said_yes = map(lambda entry: set(''.join(entry)), entries)
print(sum(map(len, said_yes)))

# part 2

all_yes = map(lambda entry: set.intersection(*map(set, entry)), entries)
print(sum(map(len, all_yes)))
