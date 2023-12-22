from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from copy import deepcopy


@dataclass(frozen=True)
class XYZ:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return XYZ(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass(frozen=True)
class Brick:
    start: XYZ
    end: XYZ

    def __lt__(self, other):
        return self.z() < other.z()

    def fall(self, n):
        return Brick(self.start + XYZ(0, 0, -n), self.end + XYZ(0, 0, -n))

    def iter_xy(self):
        for x, y in product(
            range(min(self.start.x, self.end.x), max(self.start.x, self.end.x) + 1),
            range(min(self.start.y, self.end.y), max(self.start.y, self.end.y) + 1),
        ):
            yield (x, y)

    def z(self):
        return min(self.start.z, self.end.z)

    def height(self):
        return abs(self.end.z - self.start.z) + 1


def parse_input(data: str):
    bricks = []

    for line in data.splitlines():
        start, end = line.split("~")
        bricks.append(
            Brick(
                XYZ(*(int(c) for c in start.split(","))),
                XYZ(*(int(c) for c in end.split(","))),
            )
        )

    return bricks


def drop_bricks(bricks: list[Brick]) -> list[Brick]:
    xy_stack = defaultdict(int)
    dropped_bricks = []

    for brick in sorted(bricks):
        min_z = max(xy_stack.get((x, y), 0) for x, y in brick.iter_xy()) + 1
        dropped_brick = brick.fall(brick.z() - min_z)
        dropped_bricks.append(dropped_brick)
        for x, y in dropped_brick.iter_xy():
            xy_stack[x, y] = dropped_brick.z() + dropped_brick.height() - 1

    return dropped_bricks


def get_supports(
    bricks: list[Brick],
) -> tuple[dict[Brick, set[Brick]], dict[Brick, set[Brick]]]:
    z_bricks = defaultdict(list)
    for dropped_brick in bricks:
        z_bricks[dropped_brick.z()].append(dropped_brick)

    supports = defaultdict(set)
    supported_by = defaultdict(set)

    for dropped_brick in bricks:
        bricks_above = z_bricks[dropped_brick.z() + dropped_brick.height()]

        for brick_above in bricks_above:
            if len(set(brick_above.iter_xy()) & set(dropped_brick.iter_xy())) > 0:
                supports[dropped_brick].add(brick_above)
                supported_by[brick_above].add(dropped_brick)

    return supports, supported_by


def number_of_drops(
    supports: dict[Brick, set[Brick]],
    supported_by: dict[Brick, set[Brick]],
    brick: Brick,
) -> int:
    queue = [brick]

    for brick in queue:
        for support in supports[brick]:
            supported_by[support].remove(brick)
            if len(supported_by[support]) == 0:
                queue.append(support)

        for support in supported_by[brick]:
            supports[support].remove(brick)
        del supported_by[brick]
        del supports[brick]

    return len(queue) - 1


def solve_a(bricks):
    dropped_bricks = drop_bricks(bricks)
    supports, supported_by = get_supports(dropped_bricks)

    acc = 0
    for brick in dropped_bricks:
        for s in supports[brick]:
            if len(supported_by[s]) < 2:
                break
        else:
            acc += 1

    return acc


def solve_b(bricks):
    dropped_bricks = drop_bricks(bricks)
    supports, supported_by = get_supports(dropped_bricks)

    acc = 0
    for dropped_brick in dropped_bricks:
        n = number_of_drops(deepcopy(supports), deepcopy(supported_by), dropped_brick)
        acc += n

    return acc


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
