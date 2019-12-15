from dataclasses import dataclass
from functools import partial
from typing import List

LOG = False


def enable_logging():
    global LOG
    LOG = True


def disable_logging():
    global LOGa
    LOG = False


def register_opcode(name, code):
    OPCODE_TO_NAME[code] = name
    NAME_TO_OPCODE[name] = code
    return code


POINTER, IMMEDIATE = range(2)
OPCODE_TO_NAME = {}
NAME_TO_OPCODE = {}
ADD = register_opcode('ADD', 1)
MUL = register_opcode('MUL', 2)
INPUT = register_opcode('INPUT', 3)
OUTPUT = register_opcode('OUTPUT', 4)
TERMINATE = register_opcode('TERMINATE', 99)
JUMP_IF_TRUE = register_opcode('JUMP_IF_TRUE', 5)
JUMP_IF_FALSE = register_opcode('JUMP_IF_FALSE', 6)
LESS_THAN = register_opcode('LESS_THAN', 7)
EQUALS = register_opcode('EQUALS', 8)

OP_MAX_NAME_LEN = len(max(OPCODE_TO_NAME.values(), key=len))


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

    def view(self, mem, ip, neg, pos):
        return mem[ip - neg:ip + pos + 1]

    @property
    def op_len(self):
        return OPCODE_LENGTHS[self.op]


OPCODE_LENGTHS = {
    ADD: 4,
    MUL: 4,
    INPUT: 2,
    OUTPUT: 2,
    TERMINATE: 1,
    JUMP_IF_TRUE: 3,
    JUMP_IF_FALSE: 3,
    LESS_THAN: 4,
    EQUALS: 4
}
intcode_handlers = {}


def handler(f=None, code=None):
    if f is None:
        return partial(handler, code=code)

    intcode_handlers[code] = f
    return f


def parse(ip, mem):
    raw = str(mem[ip]).zfill(5)
    mode_a, mode_b, mode_c, op = map(int, [raw[0], raw[1], raw[2], raw[3:]])
    args = [mem[ip + offset] for offset in range(1, OPCODE_LENGTHS[op])]
    # note to self, never forget how much trouble the ordering of the modes caused you as a lesson to pay more
    # attention to this stuff in the future
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


_INPUT_VALUE = 5


@handler(code=INPUT)
def intcode_input(i: Info, memory: Memory, ip: int):
    memory[i.args[0]] = _INPUT_VALUE
    return incr(ip, i)


@handler(code=OUTPUT)
def intcode_output(i: Info, memory: Memory, ip: int):
    print(memory.val_from_info(i, 0))
    return incr(ip, i)


@handler(code=TERMINATE)
def intcode_terminate(i: Info, memory: Memory, ip: int):
    return term()


@handler(code=JUMP_IF_TRUE)
def intcode_jump_if_true(i: Info, memory: Memory, ip: int):
    if memory.val_from_info(i, 0):
        return set_ip(memory.val_from_info(i, 1))
    return incr(ip, i)


@handler(code=JUMP_IF_FALSE)
def intcode_jump_if_true(i: Info, memory: Memory, ip: int):
    if not memory.val_from_info(i, 0):
        return set_ip(memory.val_from_info(i, 1))
    return incr(ip, i)


@handler(code=LESS_THAN)
def intcode_less_than(i: Info, memory: Memory, ip: int):
    memory[i.args[2]] = int(memory.val_from_info(i, 0) < memory.val_from_info(i, 1))
    return incr(ip, i)


@handler(code=EQUALS)
def intcode_equals(i: Info, memory: Memory, ip: int):
    memory[i.args[2]] = int(memory.val_from_info(i, 0) == memory.val_from_info(i, 1))
    return incr(ip, i)


def call_op(ip: int, memory: Memory, i: Info):
    if LOG:
        print(f'CALL: {OPCODE_TO_NAME[i.op]:<{OP_MAX_NAME_LEN}}, MODES: {i.modes}, ARGS: {i.args}')
    if i.op not in intcode_handlers:
        raise ValueError(f'bad opcode: {i.op}')
    return intcode_handlers[i.op](i, memory, ip)


def execute(data) -> Memory:
    memory = Memory(data.copy())
    ip = 0
    while True:
        i = parse(ip, memory)
        # for implementations of the intcodes/opcodes, look above for the @handler(code=...) decorated functions
        ip, result = call_op(ip, memory, i)
        if result is None:
            continue
        elif result == RET_TERMINATE:
            break

    return memory
