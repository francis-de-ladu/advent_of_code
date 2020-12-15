from tqdm import tqdm


def speak_numbers(numbers, until):
    last_spoken = {}
    for i, number in enumerate(numbers):
        last_spoken[number] = i

    number = 0
    for i in range(i + 1, until - 1):
        # print(i, number)
        if number in last_spoken:
            last_spoken[number], number = i, i - last_spoken[number]
        else:
            last_spoken[number], number = i, 0

    return number


if __name__ == "__main__":
    with open("puzzle.txt", 'r') as input_file:
        puzzles = input_file.read().splitlines()

    sequences = [[int(number) for number in seq.split(',')] for seq in puzzles]
    answers_1 = [436, 1, 10, 27, 78, 438, 1836]
    answers_2 = [175594, 2578, 3544142, 261214, 6895259, 18, 362]

    # part 1

    for sequence, answer in zip(sequences[1:], answers_1):
        result = speak_numbers(sequence, until=2020)
        assert result == answer, \
            f"{result} is not equal to {answer}"

    print("Part1:", speak_numbers(sequences[0], until=2020))

    # part 2

    for sequence, answer in tqdm(list(zip(sequences[1:], answers_2))):
        result = speak_numbers(sequence, until=30000000)
        assert result == answer, \
            f"{result} is not equal to {answer}"

    print("Part2:", speak_numbers(sequences[0], until=30000000))
