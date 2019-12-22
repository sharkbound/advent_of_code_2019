from collections import deque
from itertools import permutations

from read import read
# from shared.intcode_old import *
from shared.intcode import IntCode


# def solve(data):
#     last_output = best_output = 0
#     inputs = deque()
#
#     set_input_provider(inputs.popleft)
#
#     @set_output_logger
#     def output(v):
#         nonlocal last_output
#         inputs.appendleft(v)
#
#     for modes in map(list, permutations(range(5))):
#         for mode in modes:
#             for part2_modes in permutations(range(5, 10)):
#                 for phase in [mode, *part2_modes]:
#                     inputs.extendleft((phase, last_output))
#
#                     execute(data.copy())
#                     best_output = max(best_output, last_output)
#         print(best_output)

def solve(data):
    best_output = 0

    for phases in permutations(range(5, 10)):
        output = []

        def output_handler(v):
            nonlocal best_output
            output.append(v)
            best_output = max(best_output, v)

        computers = [IntCode(data, [phase], foutput=output_handler, pause_on_output=True, log_state=False, debug=True)
                     for phase in phases]
        while any(not cpu.terminated for cpu in computers):
            for cpu in computers:
                # print(f'#{cpu.id} {cpu.terminated=} {cpu.waiting_on_input=} {cpu.started=} {cpu.paused=}')
                if cpu.terminated:
                    print(f'cpu #{cpu.id} is terminated')
                    continue
                if cpu.waiting_on_input and output:
                    cpu.resume(output.pop())
                elif not cpu.started:
                    cpu.run()


def main():
    data = list(map(int, read('sample1.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()
