from collections import defaultdict


def parse_input(data):
    symbols = {}

    for j, line in enumerate(data.splitlines()):
        current_number = ""
        for i, symbol in enumerate(line):
            if not symbol.isdigit():
                if current_number:
                    symbols[i - len(current_number), j] = current_number
                    current_number = ""
                if symbol != ".":
                    symbols[(i, j)] = symbol
            if symbol.isdigit():
                current_number += symbol

        if current_number:
            symbols[i - len(current_number), j] = current_number

    return symbols


def get_adjacent_symbols(data, x, y, l):
    symbols = []
    for dx in range(x - 1, x + l + 1):
        for dy in (-1, 1):
            if (dx, y + dy) in data:
                symbols.append((dx, y + dy, data[(dx, y + dy)]))

    if (x - 1, y) in data:
        symbols.append((x - 1, y, data[(x - 1, y)]))
    if (x + l, y) in data:
        symbols.append((x + l, y, data[(x + l, y)]))

    return symbols


def solve_a(data):
    acc = 0

    for (x, y), symbol in data.items():
        if symbol.isnumeric():
            for _, _, adjacent_symbol in get_adjacent_symbols(data, x, y, len(symbol)):
                if not adjacent_symbol.isnumeric():
                    acc += int(symbol)
                    break

    return acc


def solve_b(data):
    stars = defaultdict(list)
    for (x, y), symbol in data.items():
        if symbol.isnumeric():
            for xs, ys, adjacent_symbol in get_adjacent_symbols(
                data, x, y, len(symbol)
            ):
                if adjacent_symbol == "*":
                    stars[(xs, ys)].append(int(symbol))

    return sum(l[0] * l[1] for l in stars.values() if len(l) == 2)


if __name__ == "__main__":
    from sys import stdin

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
