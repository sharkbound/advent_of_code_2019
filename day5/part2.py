from read import read
from shared.intcode_old import *


def solve_part_1(data):
    set_input_provider(lambda: 5)
    return execute(data)


def main():
    data = list(map(int, read().split(',')))
    solve_part_1(data)


if __name__ == '__main__':
    main()
