from read import read_lines


def get_fuel(mass, total=0):
    fuel = int(mass / 3) - 2
    if fuel <= 0:
        return total
    return fuel + get_fuel(fuel, total)


def solve_part_2(masses):
    return sum(map(get_fuel, masses))


def main():
    data = list(map(int, read_lines()))
    print(solve_part_2(data))


if __name__ == '__main__':
    main()
