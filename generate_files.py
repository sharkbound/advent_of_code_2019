from pathlib import Path
from typing import Union

day = int(input('day? '))


def make_files(day_folder: Path, *files: Union[str, Path]):
    if not day_folder.exists():
        day_folder.mkdir(parents=True)

    for file in files:
        with open(day_folder / file, 'w') as f:
            if file.strip().lower() in {'part1.py', 'part2.py'}:
                f.write('''\
from read import read, read_lines


def solve_part_(data):
    pass


def main():
    data = read()
    print(solve_part_(data))
    
    
if __name__ == '__main__':
    main()
''')


day_folder = Path(f'day{day}/')
make_files(day_folder, 'input.txt', 'part1.py', 'part2.py', 'notes.md')
