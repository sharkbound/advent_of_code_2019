You trace the path each wire takes as it leaves the central port, one wire per 
line of text (your puzzle input)

* one wire per line of text
* each line is tracing that one wire
* The wires twist and turn, but the two wires occasionally cross paths
*  To fix the circuit, you need to find the intersection point 
    closest to the central port
* Because the wires are on a grid, use the Manhattan distance for this measurement
* While the wires do technically cross right at the central port where they 
    both start, this point does not count, 
    nor does a wire count as crossing with itself.
* use manhattan distance: abs(x1 - x2) + abs(y1 - y2)

* U<X>  -  UP     -  X = steps 
* D<X>  -  DOWN   -  X = steps
* L<X>  -  LEFT   -  X = steps
* R<X>  -  RIGHT  -  X = steps

# part 1 goal
find the intersection point closest to the central port


```text
the central port (o)
it goes right 8, up 5, left 5, and finally down 3

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then,
if the second wire's path is U7,R6,D4,L4, 
it goes up 7, right 6, down 4, and left 4

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
```

# What is the Manhattan distance from the central port to the closest intersection?