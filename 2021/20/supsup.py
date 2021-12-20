import numpy as np
from tqdm import tqdm

key = input()
image_set = set()
i = 0
try:
    while True:
        for j, pixel in enumerate(input()):
            if pixel == "#":
                image_set.add((i, j))
        i += 1
except EOFError:
    pass


class Image:
    def __init__(self, image, outside):
        self.top = min(pixel[0] for pixel in image)
        self.bottom = max(pixel[0] for pixel in image)
        self.left = min(pixel[1] for pixel in image)
        self.right = max(pixel[1] for pixel in image)
        self.image = image
        self.outside = outside

    def __contains__(self, point):
        i, j = point

        if self.top <= i <= self.bottom and \
                self.left <= j <= self.right:
            return (i, j) in self.image
        else:
            return self.outside

    def __len__(self):
        if self.outside:
            return float("inf")
        else:
            return len(self.image)

    def enhance(self):
        next_image = set()

        for i in range(self.top - 2, self.bottom + 3):
            for j in range(self.left - 2, self.right + 3):
                if key[int("".join([
                    "1" if (di, dj) in self else "0"
                    for di in range(i - 1, i + 2)
                    for dj in range(j - 1, j + 2)
                ]), 2)] == "#":
                    next_image.add((i, j))

        return Image(
            next_image,
            (self.outside and key[511] == "#")
            or (not self.outside and key[0] == "#")
        )


image = Image(image_set, False)
for i in tqdm(range(50)):
    # supsup = np.zeros((100 + 2 * i, 100 + 2 * i))
    # for x, y in image.image:
    #     supsup[x + 2, y + 3] = 1
    # for line in np.where(supsup, '#', '.'):
    #     print(''.join(line))
    # print()
    image = image.enhance()

supsup = np.zeros((100 + 2 * i, 100 + 2 * i))
for x, y in image.image:
    supsup[x + 2, y + 3] = 1
for line in np.where(supsup, '#', '.'):
    print(''.join(line))

print(len(image))
