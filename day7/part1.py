from read import read, read_lines
from shared.intcode import execute


def solve(data):
    print(data)


def main():
    data = list(map(int, read().split(',')))
    print(solve(data.copy()))


if __name__ == '__main__':
    main()
