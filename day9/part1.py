from read import read
from shared.intcode import IntCode


def solve(program):
    IntCode(program).run()


def main():
    data = list(map(int, read('quine_sample.txt').split(',')))
    solve(data)


if __name__ == '__main__':
    main()

"""
shared/intcode.py:249
Traceback (most recent call last):
  File "D:/git/advent_of_code_2019/day9/part1.py", line 15, in <module>
    main()
  File "D:/git/advent_of_code_2019/day9/part1.py", line 11, in main
    solve(data)
  File "D:/git/advent_of_code_2019/day9/part1.py", line 6, in solve
    IntCode(program).run()
  File "D:\git\advent_of_code_2019\shared\intcode.py", line 277, in run
    self.opcode_handlers[context.instr.opcode](context)
  File "D:\git\advent_of_code_2019\shared\intcode.py", line 249, in opcode_modify_rel_base
    self.rel_base += c.val(0)
  File "D:\git\advent_of_code_2019\shared\intcode.py", line 79, in val
    return self.memory.val_from_instr(self.instr, index)
  File "D:\git\advent_of_code_2019\shared\intcode.py", line 147, in val_from_instr
    return self.val(instr.args[index], instr.modes[index])
IndexError: list index out of range
"""
