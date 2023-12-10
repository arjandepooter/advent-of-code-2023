from collections import defaultdict


def parse_input(data: str):
    start = None
    edges = defaultdict(list)

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                edges[(x, y)] = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if c == "|":
                edges[(x, y)] = [(x, y - 1), (x, y + 1)]
            if c == "F":
                edges[(x, y)] = [(x, y + 1), (x + 1, y)]
            if c == "-":
                edges[(x, y)] = [(x + 1, y), (x - 1, y)]
            if c == "7":
                edges[(x, y)] = [(x - 1, y), (x, y + 1)]
            if c == "L":
                edges[(x, y)] = [(x + 1, y), (x, y - 1)]
            if c == "J":
                edges[(x, y)] = [(x - 1, y), (x, y - 1)]

    return start, edges


def get_loop(start, edges):
    current = start
    visited = set()
    loop = []

    while current not in visited:
        loop.append(current)
        visited.add(current)
        for target in edges.get(current, []):
            if current in edges.get(target, []) and target not in visited:
                current = target

    return loop


def solve_a(data):
    return len(get_loop(*data)) // 2


def flood_fill(nodes, queue, max_x, max_y):
    visited = set(nodes)
    for x, y in queue:
        if x > max_x or y > max_y or x < 0 or y < 0:
            return None
        if (x, y) in visited:
            continue

        visited.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            queue.append((x + dx, y + dy))

    return visited - set(nodes)


def solve_b(data):
    start, edges = data
    main_loop = get_loop(start, edges)
    nodes = set(main_loop)
    left, right = [], []

    for (x0, y0), (x1, y1) in zip(main_loop, main_loop[1:] + main_loop[:1]):
        dx, dy = x1 - x0, y1 - y0

        rx, ry = -dy, dx
        lx, ly = dy, -dx

        for x, y in [(x0, y0), (x1, y1)]:
            if (x + rx, y + ry) not in nodes:
                right.append((x + rx, y + ry))
            if (x + lx, y + ly) not in nodes:
                left.append((x + lx, y + ly))

    max_x, max_y = max(x for x, _ in main_loop), max(y for _, y in main_loop)
    return len(
        flood_fill(nodes, left, max_x, max_y) or flood_fill(nodes, right, max_x, max_y)
    )


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
