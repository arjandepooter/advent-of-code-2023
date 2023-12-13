def line_to_int(line):
    acc = 0
    for c in line:
        if c == "#":
            acc |= 1
        acc <<= 1
    return acc


def parse_input(data: str):
    maps = []

    for block in data.split("\n\n"):
        lines = block.splitlines()
        rows = [line_to_int(line) for line in lines]
        cols = [line_to_int(line) for line in zip(*lines)]
        maps.append((rows, cols))

    return maps


def find_symmetry_line(l, errors=0):
    for i in range(1, len(l)):
        errors_needed = errors
        for j in range(min(i, len(l) - i)):
            diffs = (l[i - j - 1] ^ l[i + j]).bit_count()
            if diffs == 1 and errors_needed > 0:
                errors_needed -= 1
            elif diffs > 0:
                break
        else:
            if errors_needed == 0:
                return i


def solve_a(data):
    return sum(
        find_symmetry_line(cols) or find_symmetry_line(rows) * 100
        for rows, cols in data
    )


def solve_b(data):
    return sum(
        find_symmetry_line(cols, 1) or find_symmetry_line(rows, 1) * 100
        for rows, cols in data
    )


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
