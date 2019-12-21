from read import read
from shared.intcode_old import *
from shared.intcode import IntCode


def solve_part_1(data):
    IntCode(data, [5]).run()


def main():
    data = list(map(int, read().split(',')))
    solve_part_1(data)


if __name__ == '__main__':
    main()
