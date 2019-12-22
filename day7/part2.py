from collections import deque
from itertools import permutations

from read import read
from shared.intcode import IntCode


def solve(data):
    best_output = 0

    for phases in permutations(range(5, 10)):
        output = deque([0])

        def output_handler(v):
            nonlocal best_output
            output.append(v)
            best_output = max(best_output, v)

        computers = [IntCode(data, [phase], foutput=output_handler) for phase in phases]

        while not all(cpu.terminated for cpu in computers):
            for cpu in filter(lambda c: not c.terminated, computers):
                cpu.resume(output.popleft())

    return best_output


def main():
    data = list(map(int, read('data.txt').split(',')))
    print(solve(data))


if __name__ == '__main__':
    main()
