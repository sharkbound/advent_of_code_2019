from read import read_lines


def get_fuel(mass):
    if (fuel := int(mass / 3) - 2) <= 0:
        return 0
    return fuel + get_fuel(fuel)


def solve_part_2(masses):
    return sum(map(get_fuel, masses))


def main():
    data = list(map(int, read_lines()))
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
