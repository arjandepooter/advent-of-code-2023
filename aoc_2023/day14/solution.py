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


def tilt(stones, walls, w, h, direction="N"):
    catch = defaultdict(int)
    next_stones = []

    for x, y in stones:
        if direction == "N":
            blocking_walls = [(wx, wy) for wx, wy in walls if wx == x and wy < y]
            wx, wy = max(blocking_walls) if blocking_walls else (x, -1)
            catch[(wx, wy)] += 1
            next_stones.append((x, wy + catch[(wx, wy)]))
        if direction == "W":
            blocking_walls = [(wx, wy) for wx, wy in walls if wy == y and wx < x]
            wx, wy = max(blocking_walls) if blocking_walls else (-1, y)
            catch[(wx, wy)] += 1
            next_stones.append((wx + catch[(wx, wy)], y))
        if direction == "S":
            blocking_walls = [(wx, wy) for wx, wy in walls if wx == x and wy > y]
            wx, wy = min(blocking_walls) if blocking_walls else (x, h)
            catch[(wx, wy)] += 1
            next_stones.append((x, wy - catch[(wx, wy)]))
        if direction == "E":
            blocking_walls = [(wx, wy) for wx, wy in walls if wy == y and wx > x]
            wx, wy = min(blocking_walls) if blocking_walls else (h, y)
            catch[(wx, wy)] += 1
            next_stones.append((wx - catch[(wx, wy)], y))

    return next_stones


def calc_load(stones, h):
    return sum((h - y) for _, y in stones)


def create_lookup_tables(walls, w, h):
    walls_x = [[wx for wx, wy in walls if wy == y] for y in range(h)]
    walls_y = [[wy for wx, wy in walls if wx == x] for x in range(w)]

    lookup_north = []
    for y in range(h):
        for x in range(w):
            pass


def print_yo(stones, walls, w, h):
    stones = set(stones)
    walls = set(walls)
    for y in range(h):
        for x in range(h):
            if (x, y) in stones:
                print("0", end="")
            elif (x, y) in walls:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def solve_a(data):
    (w, h), stones, walls = data

    stones = tilt(stones, walls, w, h)
    create_lookup_tables(walls, w, h)
    return calc_load(stones, h)


def solve_b(data):
    (w, h), stones, walls = data

    states = {}
    for n in range(1_000_000_000):
        for d in ("N", "W", "S", "E"):
            stones = tilt(stones, walls, w, h, d)

        state = tuple(stones)
        if state in states:
            period = n - states[state]
            print(period)
            break

        states[state] = n

    return calc_load(stones, h)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
