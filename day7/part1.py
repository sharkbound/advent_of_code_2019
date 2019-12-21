from itertools import permutations

from read import read
from shared.intcode import IntCode


def solve(data):
    all_output = set()
    for phases in permutations(range(5)):
        last_output = 0

        def output(v):
            nonlocal last_output
            last_output = v

        for phase in phases:
            IntCode(data, [phase, last_output], foutput=output).run()

        all_output.add(last_output)

    print(max(all_output))


def main():
    data = list(map(int, read().split(',')))
    solve(data)


if __name__ == '__main__':
    main()
