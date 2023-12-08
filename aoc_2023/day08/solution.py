from itertools import cycle
from math import lcm


def parse_input(data: str):
    instructions, data = data.split("\n\n")
    nodes = {}
    for line in data.splitlines():
        cur, rest = line.split(" = ")
        left, right = rest[1:-1].split(", ")
        nodes[cur] = (left, right)
    return instructions, nodes


def solve_a(data):
    instructions, nodes = data
    cur = "AAA"
    acc = 0

    for instruction in cycle(instructions):
        if cur == "ZZZ":
            break
        left, right = nodes[cur]
        cur = left if instruction == "L" else right
        acc += 1

    return acc


def solve_b(data):
    instructions, nodes = data
    starting_nodes = [node for node in nodes if node.endswith("A")]
    freqs = []

    for cur in starting_nodes:
        acc = 0
        for instruction in cycle(instructions):
            if cur.endswith("Z"):
                break
            left, right = nodes[cur]
            cur = left if instruction == "L" else right
            acc += 1
        freqs.append(acc)

    return lcm(*freqs)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
