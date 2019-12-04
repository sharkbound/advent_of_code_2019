import re

from read import read


def is_increasing_or_eq(i):
    last = int(i[0])
    for digit in map(int, i[1:]):
        if digit < last:
            return False
        last = digit
    return True


def solve_part_1(data):
    start, end = map(int, data.split('-'))
    return sum(1 for i in map(str, range(start, end + 1)) if re.search(r'(\d)\1', i) and is_increasing_or_eq(i))


def main():
    data = read()
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
