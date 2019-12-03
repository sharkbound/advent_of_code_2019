import re
from typing import Tuple, NamedTuple, Set, Iterator

from read import read_lines


def dist(x: int, y: int) -> int:
    return abs(x) + abs(y)


class Wire(NamedTuple):
    path: Set[Tuple[int, int]]

    def collisions(self, other: 'Wire') -> int:
        for (x, y) in self.path & other.path:
            yield dist(x, y)


def turns(line: str) -> Iterator[Tuple[str, int]]:
    for direction, steps in re.findall(r'(\w)(\d+)', line):
        yield direction, int(steps)


def parse_wire(line: str) -> Wire:
    x = y = 0
    path = set()
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
            path.add((x, y))

    return Wire(path)


def solve_part_1(data):
    w1: Wire
    w2: Wire
    w1, w2 = map(parse_wire, data)
    print(min(w1.collisions(w2)))


def main():
    data = read_lines()
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
