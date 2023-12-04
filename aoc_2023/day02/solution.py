def parse_sample(sample):
    items = []
    for iitem in sample.split(", "):
        count, color = iitem.split(" ")
        items.append((int(count), color))
    return items


def parse_line(line):
    game, samples = line.split(": ")
    game = int(game.split(" ")[1])
    samples = samples.split("; ")
    samples = [parse_sample(sample) for sample in samples]
    return game, samples


def parse_input(data):
    lines = [parse_line(line) for line in data.splitlines() if line]
    return lines


def is_possible(samples, red=12, green=13, blue=14):
    for sample in samples:
        for amount, color in sample:
            if color == "red" and red < amount:
                return False
            elif color == "green" and green < amount:
                return False
            elif color == "blue" and blue < amount:
                return False
    return True


def min_amount(samples):
    red, green, blue = 0, 0, 0
    for sample in samples:
        for amount, color in sample:
            if color == "red" and red < amount:
                red = amount
            elif color == "green" and green < amount:
                green = amount
            elif color == "blue" and blue < amount:
                blue = amount
    return red, green, blue


def solve_a(data):
    acc = 0

    for game, samples in data:
        if is_possible(samples):
            acc += game

    return acc


def solve_b(data):
    acc = 0

    for _, samples in data:
        r, g, b = min_amount(samples)
        acc += r * g * b

    return acc


if __name__ == "__main__":
    from sys import stdin

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
