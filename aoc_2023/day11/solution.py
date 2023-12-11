from itertools import combinations


def parse_input(data: str):
    points = []

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                points.append((x, y))

    return points


def find_empty_rows_and_cols(points):
    min_x, max_x = min(x for x, _ in points), max(x for x, _ in points)
    min_y, max_y = min(y for _, y in points), max(y for _, y in points)

    empty_cols = set(range(min_x, max_x)) - set(x for x, _ in points)
    empty_rows = set(range(min_y, max_y)) - set(y for _, y in points)

    return list(empty_rows), list(empty_cols)


def expand_points(points, expansion_factor=2):
    empty_rows, empty_cols = find_empty_rows_and_cols(points)
    new_points = []

    for x, y in points:
        new_points.append(
            (
                x + len([c for c in empty_cols if c < x]) * (expansion_factor - 1),
                y + len([c for c in empty_rows if c < y]) * (expansion_factor - 1),
            )
        )

    return new_points


def solve_a(points):
    expanded_points = expand_points(points)

    return sum(
        abs(x1 - x2) + abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(expanded_points, 2)
    )


def solve_b(points):
    expanded_points = expand_points(points, 1_000_000)

    return sum(
        abs(x1 - x2) + abs(y1 - y2)
        for (x1, y1), (x2, y2) in combinations(expanded_points, 2)
    )


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
