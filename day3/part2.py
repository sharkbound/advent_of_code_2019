import re
from typing import Tuple, NamedTuple, Iterator, Dict

from read import read_lines


def dist(x: int, y: int) -> int:
    return abs(x) + abs(y)


class Wire(NamedTuple):
    dists: Dict[Tuple[int, int], int]


def turns(line: str) -> Iterator[Tuple[str, int]]:
    for direction, steps in re.findall(r'(\w)(\d+)', line):
        yield direction, int(steps)


def parse_wire(line: str) -> Wire:
    x = y = 0
    distances = {}
    length = 0
    for dir, steps in turns(line):
        y_off = x_off = 0
        if dir == 'U':
            y_off = 1
        elif dir == 'D':
            y_off = -1
        elif dir == 'L':
            x_off = -1
        elif dir == 'R':
            x_off = 1
        for _ in range(steps):
            x += x_off
            y += y_off
            length += 1
            if (x, y) not in distances:
                distances[x, y] = length
    return Wire(distances)


def solve_part_2(data):
    w1, w2 = map(parse_wire, data)
    return min(w1.dists[xy] + w2.dists[xy] for xy in w1.dists.keys() & w2.dists)


def main():
    data = read_lines()
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
