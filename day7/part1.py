from itertools import permutations

from read import read
from shared.intcode import IntCode
from shared.io import MaxIO, LastIO, IOEventRelay


def solve(data):
    best = MaxIO()

    for phases in permutations(range(5)):
        io = LastIO()
        for phase in phases:
            IntCode(data, IOEventRelay([phase, io.value], best, io)).run()

    print(best.max)


def main():
    data = list(map(int, read().split(',')))
    solve(data)


if __name__ == '__main__':
    main()
