from math import ceil, floor


def solve(t, d):
    D = t**2 - 4 * d
    p1 = (-t + D**0.5) / -2
    p2 = (-t - D**0.5) / -2
    return floor(p2) - ceil(p1) + 1


def solve_a(data):
    acc = 1

    for t, d in data:
        acc *= solve(t, d)

    return acc


def solve_b(data):
    t = int("".join(str(t) for t, _ in data))
    d = int("".join(str(d) for _, d in data))

    return solve(t, d)


if __name__ == "__main__":
    data = [(7, 9), (15, 40), (30, 200)]
    data = [(45, 295), (98, 1734), (83, 1278), (73, 1210)]
    print(solve_a(data))
    print(solve_b(data))
