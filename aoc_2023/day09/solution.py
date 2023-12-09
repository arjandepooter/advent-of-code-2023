def parse_line(line: str):
    return [int(c) for c in line.split(" ")]


def parse_input(data: str):
    lines = [parse_line(line) for line in data.splitlines()]
    return lines


def diffs(l: list[int]):
    return [b - a for a, b in zip(l, l[1:])]


def next_value(l):
    if all(c == 0 for c in l):
        return 0

    return l[-1] + next_value(diffs(l))


def prev_value(l):
    if all(c == 0 for c in l):
        return 0

    return l[0] - prev_value(diffs(l))


def solve_a(data):
    acc = 0

    for values in data:
        acc += next_value(values)

    return acc


def solve_b(data):
    acc = 0

    for values in data:
        acc += prev_value(values)

    return acc


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
