from read import read
from shared.intcode import IntCode


def solve_part_1(data):
    for a in range(100):
        for b in range(100):
            cpu = IntCode(data)
            cpu.memory[1:3] = a, b
            if cpu.run().memory[0] == 19690720:
                return 100 * a + b


def main():
    data = list(map(int, read().split(',')))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
