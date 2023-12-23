from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class XY:
    x: int
    y: int

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)


EAST = XY(1, 0)
WEST = XY(-1, 0)
NORTH = XY(0, -1)
SOUTH = XY(0, 1)
DIRECTIONS = (EAST, WEST, NORTH, SOUTH)


def parse_input(data: str):
    path = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            match c:
                case ">":
                    path[XY(x, y)] = (EAST,)
                case "<":
                    path[XY(x, y)] = (WEST,)
                case "^":
                    path[XY(x, y)] = (NORTH,)
                case "v":
                    path[XY(x, y)] = (SOUTH,)
                case ".":
                    path[XY(x, y)] = DIRECTIONS

    return path


def build_graph(path: dict[XY, tuple[XY]]) -> dict[XY, list[tuple[XY, int]]]:
    nodes: set[XY] = {min(path), max(path)}
    edges: dict[XY, list[tuple[XY, int]]] = defaultdict(list)

    for point in path:
        neighbours = len([point + d for d in DIRECTIONS if point + d in path])
        if neighbours > 2:
            nodes.add(point)

    for node in nodes:
        for d in path[node]:
            cur = node + d
            prev = node
            if cur not in path:
                continue

            n = 1
            while cur not in nodes:
                n += 1
                for d2 in path[cur]:
                    if cur + d2 == prev or (cur + d2) not in path:
                        continue
                    cur, prev = cur + d2, cur
                    break
                else:
                    break
            if cur in nodes:
                edges[node].append((cur, n))

    return edges


def find_max_path(
    edges: dict[XY, list[tuple[XY, int]]], cur=None, seen=frozenset()
) -> int:
    cur = cur or min(edges)

    if cur == max(edges):
        return 0
    if cur in seen:
        return None

    scores = [
        score + added
        for target, score in edges[cur]
        if (added := find_max_path(edges, target, seen | {cur})) is not None
    ]

    if len(scores):
        return max(scores)


def solve_a(data):
    edges = build_graph(data)
    return find_max_path(edges)


def solve_b(data):
    edges = build_graph({k: DIRECTIONS for k in data})
    return find_max_path(edges)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
