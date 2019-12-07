from collections import deque
from dataclasses import dataclass
from functools import partial
from typing import List

from read import read

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


"""
notes to self, and any others reading this later having trouble with index errors.
the modes are reverse of the order they appear to me in
from the example of AOC:

LINK:
https://adventofcode.com/2019/day/5

ABCDE
01002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero

i missed the  `mode of 1st parameter` detail many times over 2 days
going by param, it read like this:
ABC
 10

to 

CBA
 10

"""


@dataclass
class Info:
    op: int
    args: List[int]
    modes: List[int]

    def __eq__(self, op):
        return self.op == op

    def view(self, mem, ip, neg, pos):
        print(mem[ip - neg:ip + pos + 1])

    @property
    def op_len(self):
        return OPCODE_LENGTHS[self.op]


OPCODE_LENGTHS = {ADD: 4, MUL: 4, INPUT: 2, OUTPUT: 2, TERMINATE: 1}
intcode_handlers = {}


def handler(f=None, code=None):
    if f is None:
        return partial(handler, code=code)

    intcode_handlers[code] = f
    return f


def parse(ip, mem):
    op_len = {1: 4, 2: 4, 3: 2, 4: 2, 99: 1}
    raw = str(mem[ip]).zfill(5)
    mode_a, mode_b, mode_c, op = map(int, [raw[0], raw[1], raw[2], raw[3:]])
    args = [mem[ip + offset] for offset in range(1, op_len[op])]
    # note to self, never forget how much trouble the ordering of the modes caused you
    return Info(modes=[mode_c, mode_b, mode_a], args=args, op=op)


RET_TERMINATE, = range(1)


def incr(ip, i: 'Info'):
    return ip + i.op_len, None


def set_ip(new_ip):
    return new_ip, None


def term():
    return -1, RET_TERMINATE


@handler(code=ADD)
def intcode_add(i: Info, memory: Memory, ip: int):
    val1 = memory.val_from_info(i, 0)
    val2 = memory.val_from_info(i, 1)
    memory[i.args[2]] = val1 + val2
    return incr(ip, i)


@handler(code=MUL)
def intcode_mul(i: Info, memory: Memory, ip: int):
    val1 = memory.val_from_info(i, 0)
    val2 = memory.val_from_info(i, 1)
    memory[i.args[2]] = val1 * val2
    return incr(ip, i)


@handler(code=INPUT)
def intcode_input(i: Info, memory: Memory, ip: int):
    memory[i.args[0]] = 1
    return incr(ip, i)


@handler(code=OUTPUT)
def intcode_input(i: Info, memory: Memory, ip: int):
    print(memory[i.args[0]])
    return incr(ip, i)


@handler(code=TERMINATE)
def intcode_terminate(i: Info, memory: Memory, ip: int):
    return term()


def execute(data):
    memory = Memory(data.copy())
    ip = 0
    while True:
        i = parse(ip, memory)
        # for implementations of the intcodes/opcodes, look above for the @handler(code=...) decorated functions
        ip, result = intcode_handlers[i.op](i, memory, ip)
        if result is None:
            continue
        elif result == RET_TERMINATE:
            break


def solve_part_1(data):
    return execute(data)


def main():
    data = list(map(int, read().split(',')))
    solve_part_1(data)


if __name__ == '__main__':
    main()
