from copy import copy
from itertools import permutations, chain

from read import read
from shared.intcode import *

enable_logging()
disable_logging()


def solve(data):
    for modes in map(list, permutations(range(5))):
        @set_output_logger
        def output(v):
            nonlocal last_output
            last_output = v

        last_output = best_output = 0
        for mode in modes:
            for extra_modes in permutations(range(5, 10)):
                for phase in [mode, *extra_modes]:
                    inputs = [last_output, phase]

                    @set_output_logger
                    def output(v):
                        nonlocal last_output
                        inputs.append(v)
                        last_output = v
                        print(f'last(trimmed): {str(last_output)[:30]}')

                    set_input_provider(inputs.pop)

                    execute(data.copy())
                    best_output = max(best_output, last_output)

            print(best_output)


def main():
    data = list(map(int, read('sample1.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()
