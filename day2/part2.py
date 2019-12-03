from collections import deque

from read import read, read_lines

op_lengths = {
    1: 4,
    2: 4,
    99: 1,
}


def solve_part_1(data):
    orig = data.copy()

    # for a in range(100):
    #     for b in range(100):
    #         data = orig.copy()
    #         data[1:3] = a, b
    #         execute(data)
    #
    #         if data[0] == 19690720:
    #             return 100 * a + b

    for a in range(100):
        for b in range(100):
            data = orig.copy()
            data[1:3] = a, b
            execute(data)

            if data[0] == 19690720:
                return 100 * a + b

    return -1


def execute(data):
    i = 0
    while (op := data[i]) != 99:  # 99 is halt
        if op == 1:
            in1, in2, out = data[i + 1:i + 4]
            data[out] = data[in1] + data[in2]
        elif op == 2:
            in1, in2, out = data[i + 1:i + 4]
            data[out] = data[in1] * data[in2]
        elif op == 99:
            break
        i += op_lengths[op]


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
