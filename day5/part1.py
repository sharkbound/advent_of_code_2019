from collections import deque

from read import read


def expand(code):
    # ABC < modes  DE < opcode
    code = str(code).zfill(5)
    return int(code[0]), int(code[1]), int(code[2]), int(code[3:])


def param(v, mode, data):
    return v if mode else data[v]


def execute(data, inputs: deque):
    data = data.copy()
    op_lengths = dict(zip((1, 2, 3, 4), (4, 4, 2, 2)))
    ip = 0
    while True:
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
            data[data[ip + 1]] = inputs.popleft()
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
