from collections import deque
from dataclasses import dataclass
from typing import List

from read import read

TESTING = False
POINTER, IMMEDIATE = range(2)
ADD, MUL, INPUT, OUTPUT, TERMINATE = 1, 2, 3, 4, 99


class Memory:
    def __init__(self, data=()):
        self._data = list(data)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def val(self, value, mode):
        return value if mode == IMMEDIATE else self._data[value]


@dataclass
class Info:
    modes: List[int]
    args: List[int]
    op: int

    def arg_info(self, i):
        return self.args[i], self.modes[i]

    def mode(self, index):
        return self.modes[index]

    def arg(self, index):
        return self.args[index]

    def __eq__(self, op):
        return self.op == op

    def view(self, ip, neg, pos):
        print(self[ip - neg:ip + pos + 1])

    @property
    def op_len(self):
        return OPCODE_LENGTHS[self.op]


OPCODE_LENGTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, TERMINATE: 1}


def parse(ip, mem):
    op_len = {1: 4, 2: 4, 3: 2, 4: 2, 99: 1}
    raw = str(mem[ip]).zfill(5)
    mode_a, mode_b, mode_c, op = map(int, [raw[0], raw[1], raw[2], raw[3:]])
    args = [mem[ip + offset] for offset in range(1, op_len[op])]
    return Info(modes=[mode_a, mode_b, mode_c], args=args, op=op)


def execute(data, inputs: deque):
    memory = Memory(data.copy())
    ip = 0
    while True:
        info = parse(ip, memory)

        if info == ADD:
            val1 = memory.val(*info.arg_info(0))
            val2 = memory.val(*info.arg_info(1))
            memory[memory[info.arg(2)]] = val1 + val2
        elif info == MUL:
            val1 = memory.val(*info.arg_info(0))
            val2 = memory.val(*info.arg_info(1))
            memory[memory[info.arg(2)]] = val1 * val2
        elif info == INPUT:
            memory[memory[info.arg(0)]] = inputs.popleft()
        elif info == OUTPUT:
            print(memory[memory[info.arg(0)]])
        elif info == TERMINATE:
            break

        ip += info.op_len


def solve_part_1(data):
    if TESTING:
        data = [1002, 4, 3, 4, 33]
    return execute(data, deque([1]))


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
