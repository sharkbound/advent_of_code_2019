from dataclasses import dataclass, field
from typing import List

import numpy as np

from read import read


@dataclass(frozen=True)
class Layer:
    width: int
    height: int
    raw: np.ndarray
    data: np.ndarray

    @property
    def size(self):
        return self.width * self.height

    def __getitem__(self, row_index: int) -> np.ndarray:
        return self.data[row_index]


@dataclass()
class Image:
    width: int
    height: int
    raw_data: np.ndarray
    layers: List[Layer] = field(default=list)

    def __post_init__(self):
        self.layers = [
            Layer(self.width, self.height, arr.flatten(), arr)
            for arr in map(np.array, [
                self.raw_data[i:i + self.chunk_size].reshape((self.height, self.width))
                for i in range(0, len(self.raw_data), self.chunk_size)
            ])
        ]

    @property
    def chunk_size(self):
        return self.width * self.height

    def __getitem__(self, layer_index: int) -> Layer:
        return self.layers[layer_index]

    def __iter__(self) -> Layer:
        for row_index in range(len(self.raw_data) // self.chunk_size):
            yield self[row_index]


def solve(data):
    image = Image(25, 6, data)
    best = min(image.layers, key=lambda l: sum(l.raw == 0))
    print(sum(best.raw == 1) * sum(best.raw == 2))


def main():
    data = np.array(tuple(map(int, read())))
    solve(data)


if __name__ == '__main__':
    main()
