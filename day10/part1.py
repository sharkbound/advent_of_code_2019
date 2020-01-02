import numpy as np

from read import read_lines


def solve(data: np.ndarray):
    print(data.shape)


def main():
    data = np.array(tuple(map(list, read_lines())))
    solve(data)


if __name__ == '__main__':
    main()
