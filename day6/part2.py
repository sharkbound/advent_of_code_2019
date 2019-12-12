from collections import defaultdict

from read import read_lines


def path_to_root(orbits, start):
    """
    walks the path from the `start` node to the root node
    keep doing this until we cannot find any more parents
    """
    path = [start]
    cur = start
    # python 3.8 "walrus operator" is used here to make the loop more condensed
    while cur := find_parent(orbits, cur):
        path.append(cur)
    path.reverse()
    return path


def path_len(path: list, start: str):
    """
    returns the length of the given path, starting from node `start`
    skip the last node using -1 in the slice because that in the node of interest (aka SAN or YOU)
    """
    return len(path[path.index(start):-1])


def find_parent(orbits, start) -> str:
    """
    tries to find the parent of `start` node
    we go about doing this by going through the orbit dict and looking for it in the it's sub-orbits
    when we find one return that parent node
    if no parent node is found, return None
    """
    return next((key for key, value in orbits.items() if start in value), None)


def solve(data):
    # contains the sub-orbits of nodes
    orbits = defaultdict(list)
    # get all orbits in input
    for o1, o2 in (s.split(')') for s in data):
        # appends the orbit to its parent in the defaultdict
        orbits[o1].append(o2)

    # get the paths to the locations of interest
    path_to_you = path_to_root(orbits, 'YOU')
    path_to_san = path_to_root(orbits, 'SAN')

    # store path lengths to find lowest length after loop
    counts = []
    # loop over all the the common nodes in the paths
    # convert the paths the SET's to allow use of SET INTERSECTION to find all common path nodes
    for common in set(path_to_you) & set(path_to_san):
        # get the total path length,
        total = path_len(path_to_you, common) + path_len(path_to_san, common) - 2
        # add the path total path length to the path length list to min later
        counts.append(total)
        # python 3.8 f-string debug print, optional
        print(f'{common=} {total=}')
    # print the best(MIN) path length found
    return f'==================\nBEST = {min(counts)}\n=================='


def main():
    data = read_lines()
    print(solve(data))


if __name__ == '__main__':
    main()
