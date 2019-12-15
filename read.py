from typing import Iterator


def read(filename='data.txt') -> str:
    with open(filename) as f:
        return f.read()


def read_lines(filename='data.txt') -> Iterator[str]:
    with open(filename) as f:
        yield from filter(None, map(str.strip, f))
