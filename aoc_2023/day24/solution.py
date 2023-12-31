from dataclasses import dataclass
from itertools import combinations
from math import isqrt


@dataclass(frozen=True)
class XYZ:
    x: int
    y: int
    z: int

    def __len__(self):
        return self.x + self.y + self.z

    def __add__(self, other):
        return XYZ(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return self + -1 * other

    def __rmul__(self, other):
        return XYZ(other * self.x, other * self.y, other * self.z)


@dataclass
class Particle:
    position: XYZ
    velocity: XYZ

    def dxy(self):
        dy = self.velocity.y / self.velocity.x
        y0 = self.position.y - dy * self.position.x
        return (dy, y0)


def parse_input(data: str):
    particles = []

    for line in data.splitlines():
        pos, velocity = line.split(" @ ")
        pos = XYZ(*(int(c) for c in pos.split(", ")))
        velocity = XYZ(*(int(c) for c in velocity.split(", ")))
        particles.append(Particle(pos, velocity))

    return particles


def solve_a(data):
    lower = 200000000000000
    upper = 400000000000000

    acc = 0
    for p_1, p_2 in combinations(data, 2):
        dy_1, y0_1 = p_1.dxy()
        dy_2, y0_2 = p_2.dxy()

        if dy_1 == dy_2:
            continue

        x = (y0_1 - y0_2) / (dy_2 - dy_1)
        y = dy_1 * x + y0_1
        t_1 = (x - p_1.position.x) / p_1.velocity.x
        t_2 = (x - p_2.position.x) / p_2.velocity.x

        if lower <= x <= upper and lower <= y <= upper and t_1 >= 0 and t_2 >= 0:
            acc += 1

    return acc


def get_divisors(n):
    for i in range(1, isqrt(abs(n)) + 1):
        if n % i == 0:
            yield i
            yield n // i


def find_delta(d: list[tuple[int, int]]):
    result = None
    for (s0, d0), (s1, d1) in combinations(d, 2):
        if d0 != d1:
            continue
        ds = set(
            [d0 - div for div in get_divisors(s1 - s0)]
            + [d0 + div for div in get_divisors(s1 - s0)]
        )

        if result is None:
            result = ds
        else:
            result &= ds
            if len(result) == 1:
                break

    return list(result)[0]


def solve_b(data: list[Particle]):
    dx = find_delta((p.position.x, p.velocity.x) for p in data)
    dy = find_delta((p.position.y, p.velocity.y) for p in data)
    dz = find_delta((p.position.z, p.velocity.z) for p in data)
    velocity = XYZ(dx, dy, dz)

    # find 2 points which are parallel x over t
    p1 = p2 = None
    for p1, p2 in combinations(data, 2):
        if p1.velocity.x == p2.velocity.x:
            break

    dt = p1.position.x // (dx - p1.velocity.x) - p2.position.x // (dx - p2.velocity.x)
    # dt * dz = (a1 * t + b1) - (a2 * (t-dt) + b2)
    # t = (dt * dz - b1 - a2 * dt + b2) / (a1 - a2)
    # z = b1 - 2t - t * dz
    t = (dt * dz - p1.position.z - p2.velocity.z * dt + p2.position.z) // (
        p1.velocity.z - p2.velocity.z
    )
    initial_position = t * p1.velocity + p1.position - t * velocity

    return len(initial_position)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
