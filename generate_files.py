from os import PathLike
from pathlib import Path
from typing import Union

day = int(input('day? '))


def make_files(day_folder: Path, *files: Union[str, Path]):
    if not day_folder.exists():
        day_folder.mkdir(parents=True)

    for file in files:
        open(day_folder / file, 'w').close()


day_folder = Path(f'day{day}/')
make_files(day_folder, 'input.txt', 'part1.py', 'part2.py')
