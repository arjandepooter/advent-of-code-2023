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
                symbols.append(data[(dx, y + dy)])

    if (x - 1, y) in data:
        symbols.append(data[(x - 1, y)])
    if (x + l, y) in data:
        symbols.append(data[(x + l, y)])

    return symbols


def solve_a(data):
    acc = 0

    for (x, y), symbol in data.items():
        if symbol.isnumeric():
            for adjacent_symbol in get_adjacent_symbols(data, x, y, len(symbol)):
                if not adjacent_symbol.isnumeric():
                    acc += int(symbol)
                    break

    return acc


def solve_b(data):
    acc = 0
    for (x, y), symbol in data.items():
        if symbol == "*":
            numbers = [
                part for part in get_adjacent_symbols(data, x, y, 1) if part.isnumeric()
            ]
            # ouch
            numbers += [
                part
                for part in get_adjacent_symbols(data, x - 1, y, 1)
                if part.isnumeric() and len(part) == 2
            ]
            numbers += [
                part
                for part in get_adjacent_symbols(data, x - 2, y, 1)
                if part.isnumeric() and len(part) == 3
            ]
            numbers = list(set(numbers))

            if len(numbers) == 2:
                acc += int(numbers[0]) * int(numbers[1])

    return acc


if __name__ == "__main__":
    from sys import stdin

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
