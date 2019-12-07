https://adventofcode.com/2019/day/5#part2

opcodes for part 2
 * 5 - jump if true
    * params
        * 0: if is non-zero, it sets the instruction pointer to the value from the second parameter.
        * 1: what the pointer jumps to if param 0 is non-zero

 * 6 - jump if false
    * params
        * 0: if is zero, it sets the instruction pointer to the value from the second parameter.
        * 1: what the pointer jumps to if param 0 is zero