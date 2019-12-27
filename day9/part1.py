from read import read


def solve(program):
    print(program)


def main():
    data = list(map(int, read().split(',')))
    solve(data)


if __name__ == '__main__':
    main()
