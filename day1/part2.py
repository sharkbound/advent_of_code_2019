from read import read_lines


def get_fuel(mass):
    if (fuel := mass // 3 - 2) <= 0:
        return 0
    return fuel + get_fuel(fuel)


def solve_part_2(masses):
    return sum(map(get_fuel, masses))


def main():
    data = list(map(int, read_lines()))
    print(solve_part_2(data))


if __name__ == '__main__':
    main()

    # fib lambda using walrus, idk ether, but its neat
    # f = lambda n: [(a := 0), (b := 1)] + \
    #               [(c := a) + (a := b) + (b := a + c) - a - c for _ in range(n - 2)]
    # print(*f(100), sep='\n')
