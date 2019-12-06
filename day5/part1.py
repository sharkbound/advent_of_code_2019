from collections import deque

from read import read

REF, IMM = range(2)


class Memory:
    def __init__(self, data=()):
        self.data = list(data)

    def __getitem__(self, item):
        return self.data[item]

    def val(self, value, mode):
        return value if mode == IMM else self.data[value]


def expand(code):
    # ABC < modes  DE < opcode
    code = str(code).zfill(5)
    return int(code[0]), int(code[1]), int(code[2]), int(code[3:])


def param(v, mode, data):
    return v if mode else data[v]


def execute(data, inputs: deque):
    data = data.copy()
    ip = 0
    while True:
        ipval = data[ip]
        am, bm, cm, op = expand(data[ip])
        if op == 1:
            a, b, c = data[ip + 1:ip + 4]
            data[c] = param(a, am, data) + param(b, bm, data)
            ip += 4
        elif op == 2:
            a, b, c = data[ip + 1:ip + 4]
            data[c] = param(a, am, data) * param(b, bm, data)
            ip += 4
        elif op == 3:
            a = data[ip + 1]
            data[a] = inputs.popleft()
            ip += 2
        elif op == 4:
            if a := param(data[ip + 1], am, data):
                chunk = data[ip - 4:ip + 5]
                code = data[ip:ip + 2]
                print('---------------------------\n'
                      f'TEST FAILED ON {ip=}\nit was supposed to be 0\nit was actually {a=}\ncode surrounding it: {chunk=}\nthis byte code: {code=}'
                      f'\n---------------------------')
                # breakpoint()
            ip += 2
        elif op == 99:
            break
        else:
            raise ValueError(f'bad opcode: {op}')

    return data


def solve_part_1(data):
    if False:
        data = [1002, 4, 3, 4, 33]
    return execute(data, deque([1]))


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
