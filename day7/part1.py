from copy import copy
from itertools import permutations

from read import read
from shared.intcode import *


def solve(data):
    all_output = set()
    for perms in permutations(range(5)):
        perms = list(perms)
        last_output = 0

        @set_output_logger
        def output(v):
            nonlocal last_output
            last_output = v
            # print(v)

        for perm in perms:
            input_queue = [last_output, perm]
            set_input_provider(input_queue.pop)
            data = copy(data)
            execute(data)

        all_output.add(last_output)

    print(max(all_output))


def main():
    data = list(map(int, read().split(',')))
    solve(data)


if __name__ == '__main__':
    main()
