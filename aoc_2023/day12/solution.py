from functools import cache


def parse_input(data: str):
    lines = []
    for line in data.splitlines():
        pattern, amounts = line.split(" ")
        amounts = tuple(int(c) for c in amounts.split(","))
        lines.append((pattern, amounts))

    return lines


@cache
def poss(pattern, amounts, is_ending=False):
    if len(pattern) == 0:
        return 1 if len(amounts) == 0 else 0
    if len(amounts) == 0:
        return 1 if all(c != "#" for c in pattern) else 0

    if pattern.startswith("."):
        return poss(pattern[1:], amounts)

    if is_ending:
        return poss(pattern[1:], amounts) if pattern[0] != "#" else 0

    cur = amounts[0]
    res = 0
    if all(c != "." for c in pattern[:cur]) and len(pattern) >= cur:
        res += poss(pattern[cur:], amounts[1:], True)
    if pattern[0] != "#":
        res += poss(pattern[1:], amounts)

    return res


def solve_a(data):
    return sum(poss(*n) for n in data)


def solve_b(data):
    acc = 0

    for pattern, amounts in data:
        pattern = "?".join([pattern] * 5)
        amounts = amounts * 5

        acc += poss(pattern, amounts)

    return acc


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
