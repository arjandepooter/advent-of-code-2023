from collections import defaultdict


def parse_input(data: str):
    lines = data.splitlines()
    dimensions = len(lines[0]), len(lines)
    stones = []
    walls = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            match c:
                case "O":
                    stones.append((x, y))
                case "#":
                    walls.append((x, y))

    return dimensions, stones, walls


def tilt(stones, lookup_table, direction):
    dx, dy = direction
    next_stones = []
    wall_hits = defaultdict(int)
    for x, y in stones:
        wx, wy = lookup_table[(x, y)]
        wall_hits[(wx, wy)] += 1
        next_stones.append(
            (wall_hits[(wx, wy)] * dx + wx, wall_hits[(wx, wy)] * dy + wy)
        )

    next_stones.sort()
    return next_stones


def calc_load(stones, h):
    return sum((h - y) for _, y in stones)


def create_lookup_tables(walls, w, h):
    walls_x = [[wx for wx, wy in walls if wy == y] for y in range(h)]
    walls_y = [[wy for wx, wy in walls if wx == x] for x in range(w)]

    lookup_north, lookup_west, lookup_south, lookup_east = {}, {}, {}, {}
    for y in range(h):
        for x in range(w):
            blocking_walls = [wy for wy in walls_y[x] if wy < y] + [-1]
            lookup_north[(x, y)] = (x, max(blocking_walls))
            blocking_walls = [wx for wx in walls_x[y] if wx < x] + [-1]
            lookup_west[(x, y)] = (max(blocking_walls), y)
            blocking_walls = [wy for wy in walls_y[x] if wy > y] + [h]
            lookup_south[(x, y)] = (x, min(blocking_walls))
            blocking_walls = [wx for wx in walls_x[y] if wx > x] + [w]
            lookup_east[(x, y)] = (min(blocking_walls), y)

    return lookup_north, lookup_west, lookup_south, lookup_east


def solve_a(data):
    (w, h), stones, walls = data
    lookup_table, *_ = create_lookup_tables(walls, w, h)

    stones = tilt(stones, lookup_table, (0, 1))

    return calc_load(stones, h)


def solve_b(data):
    (w, h), stones, walls = data
    lookup_tables = create_lookup_tables(walls, w, h)

    states = []
    while stones not in states:
        states.append(stones)
        for l, d in zip(lookup_tables, ((0, 1), (1, 0), (0, -1), (-1, 0))):
            stones = tilt(stones, l, d)

    cycle_start = states.index(stones)
    period = len(states) - cycle_start

    return calc_load(states[cycle_start + ((1_000_000_000 - cycle_start) % period)], h)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
