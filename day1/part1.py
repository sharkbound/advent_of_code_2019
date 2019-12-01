from read import read_lines


def get_fuel(mass):
    return mass // 3 - 2


def solve_part_1(masses):
    return sum(map(get_fuel, masses))


def main():
    data = list(map(int, read_lines()))
    print(solve_part_1(data))


if __name__ == '__main__':
    main()
