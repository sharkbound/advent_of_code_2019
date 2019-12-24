# %%

from collections import Counter
from itertools import zip_longest

from read import read
import numpy as np


def solve(data):
    # arrs = np.array([np.array(chunk) for chunk in zip_longest([iter(data)] * (6 * 24))])
    # print(arrs)
    # layers = np.resize(data, (..., 24))
    # layer = min(layers, key=lambda r: sum(not x for x in r))
    # count = Counter(layer)
    # print(count)
    # return count[1] * count[2]
    #


def main():
    data = list(map(int, read()))
    print(solve(data))


if __name__ == '__main__':
    main()
