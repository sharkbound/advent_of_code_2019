import re

from read import read


def has_double(i):
    return any(m for m in re.finditer(r'(\d)(\1+)', i) if len(''.join(m.groups())) == 2)


def solve_part_2(data):
    start, end = map(int, data.split('-'))
    return sum(1 for i in map(str, range(start, end + 1)) if (has_double(i) and ''.join(sorted(i)) == i))


def main():
    data = read()
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
