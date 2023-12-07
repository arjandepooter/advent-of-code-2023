from collections import Counter
from functools import cmp_to_key


CARDS = "23456789TJQKA"


def parse_input(data: str):
    result = []
    for line in data.splitlines():
        cards, bet = line.split(" ")
        result.append((cards, int(bet)))
    return result


def compare_hands(hand1, hand2):
    for c1, c2 in zip(
        sorted(Counter(hand1).values(), reverse=True),
        sorted(Counter(hand2).values(), reverse=True),
    ):
        if c1 != c2:
            return c1 - c2
    for card1, card2 in zip(hand1, hand2):
        if card1 != card2:
            return CARDS.index(card1) - CARDS.index(card2)


def replace_joker(count: Counter):
    jokers = count.pop("J", 0)
    if count.total() == 0:
        return {"J": jokers}
    key, _ = count.most_common()[0]
    count[key] += jokers

    return count


def compare_hands_with_joker(hand1, hand2):
    card_order = "J" + CARDS.replace("J", "")
    count1 = replace_joker(Counter(hand1))
    count2 = replace_joker(Counter(hand2))

    for c1, c2 in zip(
        sorted(count1.values(), reverse=True),
        sorted(count2.values(), reverse=True),
    ):
        if c1 != c2:
            return c1 - c2
    for card1, card2 in zip(hand1, hand2):
        if card1 != card2:
            return card_order.index(card1) - card_order.index(card2)


def solve_a(data):
    compare = lambda hand: cmp_to_key(compare_hands)(hand[0])

    return sum(i * bet for i, (_, bet) in enumerate(sorted(data, key=compare), 1))


def solve_b(data):
    compare = lambda hand: cmp_to_key(compare_hands_with_joker)(hand[0])

    return sum(i * bet for i, (_, bet) in enumerate(sorted(data, key=compare), 1))


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
