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

    def __getitem__(self, item: int):
        return self._data[item]

    def __setitem__(self, key: int, value: int):
        self._data[key] = value

    def val(self, value: int, mode: int):
        if mode == IMMEDIATE:
            return value
        return self[value]

    def val_from_info(self, info: 'Info', index: int):
        return self.val(info.args[index], info.modes[index])


@dataclass
class Info:
    op: int
    args: List[int]
    modes: List[int]

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
        i = parse(ip, memory)
        print(i)
        if i == ADD:
            val1 = memory.val_from_info(i, 0)
            val2 = memory.val_from_info(i, 1)
            memory[i.args[2]] = val1 + val2
        elif i == MUL:
            val1 = memory.val_from_info(i, 0)
            val2 = memory.val_from_info(i, 1)
            memory[i.args[2]] = val1 * val2
        elif i == INPUT:
            memory[i.args[0]] = inputs.popleft()
        elif i == OUTPUT:
            print(memory[i.args[0]])
        elif i == TERMINATE:
            break

        ip += i.op_len


def solve_part_1(data):
    if TESTING:
        data = [1002, 4, 3, 4, 33]
    return execute(data, deque([1]))


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
