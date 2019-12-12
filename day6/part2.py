from collections import defaultdict, deque

from read import read_lines


# def iter_orbit_branches(orbits):
#     total = 0
#     for base_orbit in orbits:
#         queue = deque([base_orbit])
#         while queue:
#             value = queue.popleft()
#             subs = orbits.get(value, [])
#             total += len(subs)
#             queue.extend(subs)
#
#     return total

def walk_orbits(orbits):
    print(orbits)


def path_to_root(orbits, start):
    path = [start]
    cur = start
    while cur := find_parent(orbits, cur):
        path.append(cur)
    path.reverse()
    return path


YOU, SAN = 'YOU', 'SAN'


def path_len(path: list, start: str, sub=0):
    l = path[path.index(start):-1]
    # print(f'{l} {len(l)-sub} {sub}')
    return len(l) - sub


def solve(data):
    orbits = defaultdict(list)
    for o1, o2 in (s.split(')') for s in data):
        orbits[o1].append(o2)

    py = path_to_root(orbits, YOU)
    ps = path_to_root(orbits, SAN)

    counts = []
    for common in set(py) & set(ps):
        total = path_len(py, common, 1) + path_len(ps, common, 1)
        counts.append(total)
        print(f'{common=} {total=}')

    return f'==================\nBEST = {min(counts)}\n=================='
    # print(f'{py}\n{ps}')


def find_parent(orbits, to_find) -> str:
    return next((key for key, value in orbits.items() if to_find in value), None)


def main():
    data = read_lines()
    print(solve(data))


if __name__ == '__main__':
    main()
