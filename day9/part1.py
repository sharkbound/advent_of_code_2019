from read import read
from shared.intcode import IntCode
from shared.io import basic_input


def solve(program):
    IntCode(program, basic_input(1), debug=True).run()


def main():
    data = list(map(int, read('data.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()
