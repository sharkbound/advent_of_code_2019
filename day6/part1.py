from collections import defaultdict, deque

from read import read_lines


def solve(data):
    orbits = defaultdict(list)
    for o1, o2 in (s.split(')') for s in data):
        orbits[o1].append(o2)

    # i use a iterative approach as recursion is slower in python due to python not doing tail-call-optimization
    # i also think this way is less conventional
    # in addition looks neater than the recursive function
    # i also forced myself to do this to learn more approaches to solving these sort of problems

    total = 0
    # we need the total for all nodes that have any orbiting planet (aka is in the dict)
    for base_orbit in orbits:
        # initialize the queue with the starting point node
        queue = deque([base_orbit])
        # loop while we have any orbits left
        while queue:
            # grab the next orbit in line to be checked,
            value = queue.popleft()
            # this is where we get the nodes orbiting the current node
            # this is needed to keep going while there is orbiting nodes to check
            subs = orbits.get(value, [])
            # adding the length of the sub-nodes to total is how we keep the running orbit count
            # the value of subs will always be the nodes that orbit the current node
            total += len(subs)
            # push the sub-nodes orbiting the current node to the queue to be search through in the next iteration
            queue.extend(subs)
    # at this point all the nodes have been checked, and the orbits summed, so we just need to return it to be printed
    return total


def main():
    data = read_lines()
    print(solve(data))


if __name__ == '__main__':
    main()
