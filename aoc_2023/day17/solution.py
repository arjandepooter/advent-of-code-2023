from dataclasses import dataclass, field
from heapq import *


@dataclass(eq=True, frozen=True)
class XY:
    x: int
    y: int

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def rotate_cw(self):
        return XY(-self.y, self.x)

    def rotate_ccw(self):
        return XY(self.y, -self.x)


@dataclass(frozen=True, eq=True)
class State:
    position: XY
    direction: XY

    def __lt__(self, other):
        return True


def parse_input(data: str):
    return [[int(c) for c in line] for line in data.splitlines()]


def in_grid(grid, xy: XY):
    w, h = len(grid[0]), len(grid)

    return 0 <= xy.x < w and 0 <= xy.y < h


def find_cost(grid, min_forward, max_forward):
    w, h = len(grid[0]), len(grid)
    queue = [(0, State(XY(0, 0), XY(1, 0))), (0, State(XY(0, 0), XY(0, 1)))]
    heapify(queue)
    seen = {}

    while queue:
        cost, state = heappop(queue)
        if state in seen and seen[state] <= cost:
            continue

        seen[state] = cost

        new_cost = cost
        target = state.position
        for n in range(1, max_forward + 1):
            target += state.direction
            if not in_grid(grid, target):
                continue
            new_cost += grid[target.y][target.x]

            if n >= min_forward:
                heappush(queue, (new_cost, State(target, state.direction.rotate_cw())))
                heappush(queue, (new_cost, State(target, state.direction.rotate_ccw())))

    for state, cost in seen.items():
        if state.position.x == (w - 1) and state.position.y == (h - 1):
            return cost


def solve_a(data):
    return find_cost(data, 0, 3)


def solve_b(data):
    return find_cost(data, 4, 10)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
