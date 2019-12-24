from read import read
from shared.intcode import IntCode
from shared.io import IO


def solve_part_1(data):
    IntCode(data, IO([5])).run()


def main():
    data = list(map(int, read().split(',')))
    solve_part_1(data)


if __name__ == '__main__':
    main()
