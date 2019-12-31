from read import read
from shared.intcode import IntCode
from shared.io import IO


def solve(program):
    IntCode(program, IO([1])).run()


def main():
    data = list(map(int, read('data.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()
