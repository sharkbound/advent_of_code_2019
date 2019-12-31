from typing import Iterable

from read import read
from shared.intcode import IntCode
from shared.io import IO


def test_intcode_day9_1():
    assert IntCode([109, -1, 4, 1, 99]).run().output == -1


def test_intcode_day9_2():
    assert IntCode([109, -1, 104, 1, 99]).run().output == 1


def test_intcode_day9_3():
    assert IntCode([109, -1, 204, 1, 99]).run().output == 109


def test_intcode_day9_4():
    assert IntCode([109, 1, 9, 2, 204, -6, 99]).run().output == 204


def test_intcode_day9_5():
    assert IntCode([109, 1, 109, 9, 204, -6, 99]).run().output == 204


def test_intcode_day9_6():
    assert IntCode([109, 1, 209, -1, 204, -106, 99]).run().output == 204


def test_intcode_day9_7():
    IN = 1336
    assert IntCode([109, 1, 3, 3, 204, 2, 99], IO.from_args(IN)).run().output == IN


def test_intcode_day9_8():
    IN = 1337
    # print()
    assert IntCode([109, 1, 203, 2, 204, 2, 99], IO.from_args(IN), debug=True).run().output == IN
