from dataclasses import dataclass
from functools import cache
from heapq import heapify, heappop, heappush


@dataclass(frozen=True)
class XY:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)


def parse_input(data: str):
    walls = set()
    start = None
    lines = data.splitlines()
    w, h = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case "#":
                    walls.add(XY(x, y))
                case "S":
                    start = XY(x, y)

    return walls, start, (w, h)


def dijkstra(walls, start, dimensions):
    w, h = dimensions
    heapify(queue := [(0, start)])
    visited = {}

    while len(queue):
        steps, point = heappop(queue)
        if (
            (point in visited and visited[point] <= steps)
            or point in walls
            or point.x < 0
            or point.x >= w
            or point.y < 0
            or point.y >= h
        ):
            continue
        visited[point] = steps

        for d in (XY(1, 0), XY(-1, 0), XY(0, 1), XY(0, -1)):
            target = point + d
            heappush(queue, (1 + steps, target))

    return visited


def solve_a(data):
    return len([s for s in dijkstra(*data).values() if s <= 64 and s % 2 == 0])


def solve_b(data):
    return 0


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
