from enum import Enum

import numpy as np

from read import read_lines


class Type(Enum):
    empty = '.'
    asteroid = '#'


def solve(data: np.ndarray):
    print(data.size, data.shape)


def main():
    data = np.array(tuple(map(list, read_lines())))
    solve(data)


if __name__ == '__main__':
    main()
