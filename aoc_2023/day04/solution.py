def parse_part(part):
    numbers = []
    for n in range(0, len(part), 3):
        numbers.append(int(part[n + 1 : n + 3].strip()))

    return numbers


def parse_line(line):
    card, numbers = line.split(":")
    card_number = int(card[5:].strip())

    part1, part2 = numbers.split(" |")
    part1 = parse_part(part1)
    part2 = parse_part(part2)
    return (card_number, part1, part2)


def parse_input(data):
    lines = [parse_line(line) for line in data.splitlines() if line]
    return lines


def solve_a(data):
    acc = 0

    for _, l1, l2 in data:
        d = set(l1) & set(l2)
        if len(d) > 0:
            acc += 2 ** (len(d) - 1)

    return acc


def solve_b(data):
    cards = [1] * len(data)

    for card, l1, l2 in data:
        won = len(set(l1) & set(l2))

        for i in range(min(won, len(cards) - won)):
            cards[card + i] += cards[card - 1]

    return sum(cards)


if __name__ == "__main__":
    from sys import stdin

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
