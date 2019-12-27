from dataclasses import dataclass, field
from typing import List

import numpy as np

from read import read

SIZE = HEIGHT, WIDTH = 6, 25


def first_non_transparent(values):
    for x in values:
        if x != 2:
            return x


def solve(data):
    layers = np.array([
        arr.reshape(SIZE)
        for arr in np.array_split(data, len(data) // (WIDTH * HEIGHT))
    ])

    final = np.zeros(SIZE)
    for i in np.ndindex(SIZE):
        final[i] = first_non_transparent(layer[i] for layer in layers)

    graph(final)


def graph(final):
    import matplotlib.pyplot as plt
    plt.imshow(final)
    plt.show()


def main():
    data = np.array(tuple(map(int, read())))
    solve(data)


if __name__ == '__main__':
    main()
