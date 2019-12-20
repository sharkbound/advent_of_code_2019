from collections import deque
from copy import copy
from itertools import permutations, chain

from read import read
from shared.intcode import *


# enable_logging()


def solve(data):
    last_output = best_output = 0
    inputs = deque([])

    set_input_provider(inputs.popleft)

    @set_output_logger
    def output(v):
        nonlocal last_output
        inputs.appendleft(v)
        print(f'last: {str(last_output)[:30]}')

    for modes in map(list, permutations(range(5))):

        for mode in modes:
            for part2_modes in permutations(range(5, 10)):
                for phase in [mode, *part2_modes]:
                    inputs.extendleft([phase, last_output])

                    execute(data.copy())
                    best_output = max(best_output, last_output)

        print(best_output)


def main():
    data = list(map(int, read('sample1.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()
