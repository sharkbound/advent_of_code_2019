import re

from read import read


def solve_part_1(data):
    start, end = map(int, data.split('-'))
    return sum(1 for i in map(str, range(start, end + 1)) if re.search(r'(\d)\1', i) and ''.join(sorted(i)) == i)


def main():
    data = read()
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
