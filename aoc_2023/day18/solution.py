from dataclasses import dataclass
from collections import Counter, defaultdict
from functools import cached_property, total_ordering


@dataclass(frozen=True)
class XY:
    x: int
    y: int

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return XY(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other


DIRS = {"U": XY(0, -1), "L": XY(-1, 0), "D": XY(0, 1), "R": XY(1, 0)}
DIRS_LIST = [XY(1, 0), XY(0, 1), XY(-1, 0), XY(0, -1)]


def parse_color(c: str):
    c = c.strip("()#")
    return int(c, 16)


def parse_input(data: str):
    digs = []
    for line in data.splitlines():
        d, l, c = line.split(" ")
        digs.append((DIRS[d], int(l), parse_color(c)))
    return digs


def get_nodes(instructions):
    current = XY(0, 0)
    nodes = []

    for d, l in instructions:
        nodes.append(current)
        current += d * l

    return nodes


def calc_fill(nodes):
    fill = 0

    # https://en.wikipedia.org/wiki/Shoelace_formula
    for a, b in zip(nodes, nodes[1:] + [nodes[0]]):
        fill += a.x * b.y - a.y * b.x
        # correct for half cells as the coordinate is in the middle of a cell, so add half length!
        fill += abs(b.x - a.x) + abs(b.y - a.y)

    return fill // 2 + 1  # correct for the 4 leftover quarters!


def solve_a(data):
    return calc_fill(get_nodes([(d, l) for d, l, _ in data]))


def solve_b(data):
    return calc_fill(get_nodes([(DIRS_LIST[c & 0xF], c >> 4) for _, _, c in data]))


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
