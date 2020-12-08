import re

# load and preprocess input puzzle

with open("puzzle.txt", 'r') as input_file:
    puzzle = input_file.read()  # .splitlines()

puzzle = re.sub(r"(\sbags?|no\sother|\.)", "", puzzle)[:-1]

rules = map(lambda x: re.split(r"(?:\scontain\s|,\s|\.)", x),
            puzzle.split('\n'))


def get_content(rule):
    if rule[1]:
        return dict(map(lambda x: (x[2:], int(x[:1])), rule[1:]))
    else:
        return 0


rules = {rule[0]: get_content(rule) for rule in rules}


# part 1

can_contain = set()
to_add = {"shiny gold"}
while len(to_add):
    can_contain = can_contain.union(to_add)
    to_add = set()
    for bag, content in rules.items():
        if not content:
            continue
        content_colors = set(content.keys())
        if bag not in can_contain and content_colors.intersection(can_contain):
            to_add.add(bag)

print(len(can_contain) - 1)


# part 2

def content_size(content):
    if content:
        return sum(map(lambda x: x[1] * (1 + content_size(rules[x[0]])),
                       content.items()))
    else:
        return 0


print(content_size(rules['shiny gold']))
