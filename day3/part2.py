import re
from typing import Tuple, NamedTuple, Iterator, Dict

from read import read_lines

GRAPH = True


def dist(x: int, y: int) -> int:
    return abs(x) + abs(y)


class Wire(NamedTuple):
    dists: Dict[Tuple[int, int], int]
    # used for graphing
    #                  dir  steps x_off, y_off total x_off  total y_off
    turns: Tuple[Tuple[str, int, int, int, int, int]]


def turns(line: str) -> Iterator[Tuple[str, int]]:
    for direction, steps in re.findall(r'(\w)(\d+)', line):
        yield direction, int(steps)


def graph(*wires):
    if not GRAPH:
        return

    import matplotlib.pyplot as plt

    colors = iter('rg')

    for wire in wires:
        color = next(colors)
        last = 0, 0

        for turn in wire.turns:
            _, _, _, _, xoff, yoff = turn
            plt.plot([last[0], last[0] + xoff], [last[1], last[1] + yoff], color)
            last = last[0] + xoff, last[1] + yoff

    plt.show()


def parse_wire(line: str) -> Wire:
    x = y = 0
    distances = {}
    length = 0
    wire_turns = []
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
        wire_turns.append((dir, steps, x_off, y_off, x_off * steps, y_off * steps))
        for _ in range(steps):
            x += x_off
            y += y_off
            length += 1
            if (x, y) not in distances:
                distances[x, y] = length
    return Wire(distances, tuple(wire_turns))


def solve_part_2(data):
    w1, w2 = map(parse_wire, data)
    graph(w1, w2)
    return min(w1.dists[xy] + w2.dists[xy] for xy in w1.dists.keys() & w2.dists)


def main():
    data = read_lines()
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
