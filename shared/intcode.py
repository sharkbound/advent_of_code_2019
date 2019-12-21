from collections import deque
from copy import deepcopy
from typing import Dict, Callable, NamedTuple, List, Union, Iterable


class Instruction(NamedTuple):
    opcode: int
    args: List[int]
    modes: List[int]

    def __eq__(self, opcode):
        return self.opcode == opcode

    def view(self, mem, ip, neg, pos):
        return mem[ip - neg:ip + pos + 1]

    def __len__(self):
        return OPCODE_LENGTHS[self.opcode]


def register_opcode(name, code, length):
    OPCODE_TO_NAME[code] = name
    NAME_TO_OPCODE[name] = code
    OPCODE_LENGTHS[code] = length
    return code


POINTER, IMMEDIATE = range(2)

OPCODE_TO_NAME = {}
NAME_TO_OPCODE = {}
OPCODE_LENGTHS = {}

ADD = register_opcode('ADD', code=1, length=4)
MUL = register_opcode('MUL', code=2, length=4)
INPUT = register_opcode('INPUT', code=3, length=2)
OUTPUT = register_opcode('OUTPUT', code=4, length=2)
TERMINATE = register_opcode('TERMINATE', code=99, length=1)
JUMP_IF_TRUE = register_opcode('JUMP_IF_TRUE', code=5, length=3)
JUMP_IF_FALSE = register_opcode('JUMP_IF_FALSE', code=6, length=3)
LESS_THAN = register_opcode('LESS_THAN', code=7, length=4)
EQUALS = register_opcode('EQUALS', code=8, length=4)

OP_MAX_NAME_LEN = len(max(NAME_TO_OPCODE, key=len))


class Context(NamedTuple):
    ip: int
    memory: 'Memory'
    instr: Instruction
    cpu: 'IntCode'

    def __eq__(self, opcode):
        return self.instr.opcode == opcode

    def arg(self, index):
        return self.instr.args[index]

    def val(self, index: int):
        return self.memory.val_from_instr(self.instr, index)


class Handler:
    def __init__(self, opcode: int):
        self.opcode = opcode
        self.f = None

    def __call__(self, f):
        self.f = f
        return self


class Memory:
    def __init__(self, data=()):
        self._data = list(data)

    def __getitem__(self, item: int):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def val(self, value: int, mode: int):
        if mode == IMMEDIATE:
            return value
        return self[value]

    def instruction(self, ip: int):
        raw = str(self[ip]).zfill(5)
        modes = [int(x) for x in (raw[2], raw[1], raw[0])]
        opcode = int(raw[3:])
        opcode_len = OPCODE_LENGTHS[opcode]
        args = [self[ip + offset] for offset in range(1, opcode_len)] \
            if opcode_len - 1 \
            else []
        return Instruction(opcode=opcode, args=args, modes=modes)

    def val_from_instr(self, instr: 'Instruction', index: int):
        return self.val(instr.args[index], instr.modes[index])


class IntCode:
    def __init__(self, code: list, input: Union[deque, list, tuple] = None, finput: Callable[[deque], int] = None,
                 foutput: Callable[[int], None] = None):

        if isinstance(input, Iterable):
            input = deque(input)

        self.pause_on_output = False
        self.waiting_on_input = False
        self._debug = False
        self.finput = finput or (lambda d: d.popleft())
        self.foutput = foutput or (lambda v: print(f'OUTPUT: {v}'))
        self.input = input if input is not None else deque()
        self.memory = Memory(code)
        self.ip = 0
        self.paused = False
        self.terminated = False
        self.output = None
        self._opcode_handlers: Dict[int, Callable[[Context], None]] = {}

        self._register_op_handler()

    running = property(lambda self: not self.paused and not self.terminated)

    def _incr_ip(self, c: Context):
        self.ip += len(c.instr)

    def debug(self):
        self._debug = True
        return self

    @Handler(ADD)
    def opcode_add(self, c: Context):
        c.memory[c.instr.args[2]] = c.val(0) + c.val(1)
        self._incr_ip(c)

    @Handler(MUL)
    def opcode_mul(self, c: Context):
        c.memory[c.arg(2)] = c.val(0) * c.val(1)
        self._incr_ip(c)

    @Handler(INPUT)
    def opcode_input(self, c: Context):
        if self.input:
            c.memory[c.arg(0)] = self.finput(self.input)
            self._incr_ip(c)
        else:
            self.waiting_on_input = True

    @Handler(OUTPUT)
    def opcode_output(self, c: Context):
        output = c.val(0)
        self.foutput(output)
        self.output = output

        if self.pause_on_output:
            self.paused = True

        self._incr_ip(c)

    @Handler(TERMINATE)
    def opcode_terminate(self, _):
        self.terminated = True
        # self._incr_ip(c)

    @Handler(JUMP_IF_TRUE)
    def opcode_jump_if_true(self, c: Context):
        if c.val(0):
            self.ip = c.val(1)
        else:
            self._incr_ip(c)

    @Handler(JUMP_IF_FALSE)
    def opcode_jump_if_false(self, c: Context):
        if not c.val(0):
            self.ip = c.val(1)
        else:
            self._incr_ip(c)

    @Handler(LESS_THAN)
    def opcode_less_than(self, c: Context):
        c.memory[c.arg(2)] = int(c.val(0) < c.val(1))
        self._incr_ip(c)

    @Handler(EQUALS)
    def opcode_equals(self, c: Context):
        c.memory[c.arg(2)] = int(c.val(0) == c.val(1))
        self._incr_ip(c)

    def clone(self):
        return deepcopy(self)

    def resume(self, input_value, pause_on_output=False):
        self.input.appendleft(input_value)
        self.waiting_on_input = False
        self.run(pause_on_output=pause_on_output)

    def debug_log(self, ip: int, memory: Memory, instr: Instruction):
        values = [memory.val_from_instr(instr, index) for index in range(len(instr.args))]
        print(f'IP: {ip:<8}'
              f'OPCODE({instr.opcode:0>3}): {OPCODE_TO_NAME[instr.opcode]:<{OP_MAX_NAME_LEN + 5}}'
              f'MODES: {instr.modes!r:<13}'
              f'ARGS: {instr.args!r:<18}'
              f'VALUES: {values!r:<30}')

    def run(self, pause_on_output=False):
        self.pause_on_output = pause_on_output

        while True:
            context = Context(ip=self.ip, memory=self.memory, instr=self.memory.instruction(self.ip), cpu=self)

            if self._debug:
                self.debug_log(self.ip, self.memory, context.instr)

            self._opcode_handlers[context.instr.opcode](context)
            if self.terminated or self.paused or self.waiting_on_input:
                return self

    def _register_op_handler(self):
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Handler):
                bound = v.f.__get__(self)
                self._opcode_handlers[v.opcode] = bound
                setattr(self, k, bound)


if __name__ == '__main__':
    cpu = IntCode([103, 0, 4, 0, 99], debug=False)
    cpu.run(True)
    cpu.resume('added', False)
