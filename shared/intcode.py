from copy import deepcopy
from typing import Dict, Callable, NamedTuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from shared.io import IO


class IdGenerator:
    def __init__(self):
        self.id = 0

    def __next__(self):
        id = self.id
        self.id += 1
        return id


id_generator = IdGenerator()


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


POINTER = 0
IMMEDIATE = 1
RELATIVE = 2

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
    def __init__(self, data=(), cpu: 'IntCode' = None):
        self.cpu = cpu
        self.data = list(data)

    def __getitem__(self, item: int):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def val(self, value: int, mode: int):
        if mode == IMMEDIATE:
            return value
        elif mode == RELATIVE:
            return value
        elif mode == POINTER:
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
    def __init__(self, code: list, io: 'IO' = None, debug=False, log_state=False, pause_on_output=False):
        from .io import IO
        self.pause_on_output = pause_on_output
        self.log_state = log_state
        self.waiting_on_input = False
        self.debug = debug
        self.io = io if io is not None else IO()
        self.memory = Memory(code, self)
        self.ip = 0
        self.paused = False
        self.terminated = False
        self.output = None
        self._opcode_handlers: Dict[int, Callable[[Context], None]] = {}
        self.id = next(id_generator)
        self.started = False

        self._register_op_handler()

    @property
    def running(self):
        return not self.paused and not self.terminated

    def _incr_ip(self, c: Context):
        self.ip += len(c.instr)

    @Handler(ADD)
    def opcode_add(self, c: Context):
        c.memory[c.arg(2)] = c.val(0) + c.val(1)
        self._incr_ip(c)

    @Handler(MUL)
    def opcode_mul(self, c: Context):
        c.memory[c.arg(2)] = c.val(0) * c.val(1)
        self._incr_ip(c)

    @Handler(INPUT)
    def opcode_input(self, c: Context):
        if self.io:
            value = self.io.first(self)
            if self.log_state:
                print(f'computer #{self.id} got input {value} at ip {self.ip}')
            c.memory[c.arg(0)] = value
            self._incr_ip(c)
        else:
            self.waiting_on_input = True
            self.paused = True
            if self.log_state:
                print(f'computer #{self.id} is waiting for input at ip {self.ip}')

    @Handler(OUTPUT)
    def opcode_output(self, c: Context):
        self.output = c.val(0)
        self.io.on_output(self.output, self)

        if self.log_state:
            print(f'computer #{self.id} outputted {self.output}')

        if self.pause_on_output:
            self.paused = True
            if self.log_state:
                print(f'computer #{self.id} paused at a output at ip {self.ip}')

        self._incr_ip(c)

    @Handler(TERMINATE)
    def opcode_terminate(self, _):
        self.terminated = True
        self.started = False
        if self.log_state:
            print(f'computer #{self.id} has terminated at ip {self.ip}')

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

    def resume(self, input_value):
        self.io.append(input_value)
        self.waiting_on_input = False
        self.paused = False
        self.run()

    def debug_log(self, ip: int, memory: Memory, instr: Instruction):
        values = [memory.val_from_instr(instr, index) for index in range(len(instr.args))]
        print(f'CPU#{self.id!s:<5}'
              f'IP: {ip:<8}'
              f'OPCODE({instr.opcode:0>3}): {OPCODE_TO_NAME[instr.opcode]:<{OP_MAX_NAME_LEN + 5}}'
              f'MODES: {instr.modes!r:<13}'
              f'ARGS: {instr.args!r:<18}'
              f'VALUES: {values!r:<30}')

    def run(self):
        self.started = True
        while True:
            context = Context(ip=self.ip, memory=self.memory, instr=self.memory.instruction(self.ip), cpu=self)

            if self.debug:
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
