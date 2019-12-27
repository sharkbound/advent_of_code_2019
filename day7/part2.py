from itertools import permutations

from read import read
from shared.intcode import IntCode
from shared.io import IOEventRelay, MaxIO


def solve(data):
    best = MaxIO()

    for phases in permutations(range(5, 10)):
        io = MaxIO([0])
        computers = [IntCode(data, IOEventRelay([phase], io, best)) for phase in phases]

        while not all(cpu.terminated for cpu in computers):
            for cpu in filter(lambda c: not c.terminated, computers):
                cpu.resume(io.first())

    return best.max


def main():
    data = list(map(int, read('data.txt').split(',')))
    print(solve(data))


if __name__ == '__main__':
    main()
