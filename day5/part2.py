from read import read
from shared.intcode import *


def solve_part_1(data):
    return execute(data)


def main():
    data = list(map(int, read().split(',')))
    solve_part_1(data)


if __name__ == '__main__':
    main()
