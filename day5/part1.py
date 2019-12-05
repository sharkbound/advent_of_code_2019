from collections import deque

from read import read


def modes(code):
    code = str(code).zfill(5)
    return int(code[0]), int(code[1]), int(code[2]), int(code[3:])


def value(v, data, mode):
    return v if mode == 1 else data[v]


def execute(data, inputs: deque):
    data = data.copy()
    op_lengths = dict(zip((1, 2, 3, 4, 99), (4, 4, 2, 2, 1)))
    i = 0
    while True:
        am, bm, cm, op = modes(data[i])
        if op == 1:
            a, b, c = data[i + 1:i + 4]
            data[value(c - 1, data, cm)] = value(a, data, am) + value(b, data, bm)
        elif op == 2:
            a, b, c = data[i + 1:i + 4]
            data[value(c - 1, data, cm)] = value(a, data, am) * value(b, data, bm)
        elif op == 3:
            a = data[i + 1]
            data[value(a, data, am)] = inputs.popleft()
        elif op == 4:
            a = data[i + 1]
            print(data[a])
        elif op == 99:
            break
        i += op_lengths[op]

    return data


def solve_part_1(data):
    if True:
        data = [1101, 100, -1, 4, 0]
    return (execute(data, deque([1])))


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
