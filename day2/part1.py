from read import read
from shared.intcode import IntCode


def solve_part_1(data):
    data[1], data[2] = 12, 2
    print(IntCode(data).run().memory[0])


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
