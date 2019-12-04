import re

from read import read, read_lines


def solve_part_1(data):
    start, end = map(int, data.split('-'))
    password_range = range(start, end + 1)
    count = 0

    for i in map(str, password_range):
        if not re.search(r'(\d)\1', i):
            continue

        last = int(i[0])
        bad = False
        for digit in map(int, i[1:]):
            if digit < last:
                bad = True
                break
            last = digit

        if bad:
            continue

        count += 1
    return count


def main():
    data = read()
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
