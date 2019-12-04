import re

from read import read, read_lines


def solve_part_2(data):
    start, end = map(int, data.split('-'))
    password_range = range(start, end + 1)
    count = 0

    for i in map(str, password_range):
        double = False
        for m in re.finditer(r'(\d)(\1+)', i):
            s = ''.join(m.groups())
            double = double or len(s) == 2

        if not double:
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
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
