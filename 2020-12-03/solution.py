
with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read().splitlines()

trees_per_path = []
for mult in (1, 3, 5, 7, 0.5):
    path = ''.join([line[int(mult * i) % len(line)]
                    for i, line in enumerate(puzzle)
                    if mult * i == int(mult * i)])
    trees_per_path.append(path.count('#'))

print(trees_per_path)

mult_result = 1
for cnt in trees_per_path:
    mult_result *= cnt

print(mult_result)
