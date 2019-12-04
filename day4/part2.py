import re

from read import read


def is_increasing_or_eq(i):
    last = int(i[0])
    for digit in map(int, i[1:]):
        if digit < last:
            return False
        last = digit
    return True


def has_double(i):
    return any(m for m in re.finditer(r'(\d)(\1+)', i) if len(''.join(m.groups())) == 2)


def solve_part_2(data):
    start, end = map(int, data.split('-'))
    return sum(1 for i in map(str, range(start, end + 1)) if (has_double(i) and is_increasing_or_eq(i)))


def main():
    data = read()
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
