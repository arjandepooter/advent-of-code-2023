def parse_input(data):
    lines = [line for line in data.splitlines() if line]
    return lines


def solve_a(data):
    acc = 0

    for line in data:
        digits = [int(x) for x in line if x.isdigit()]
        acc += digits[0] * 10 + digits[-1]

    return acc


def solve_b(data):
    digs = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    acc = 0

    for line in data:
        digits = []
        for i, c in enumerate(line):
            if c.isdigit():
                digits.append(int(c))
            for d, val in enumerate(digs, 1):
                if line[i:].startswith(val):
                    digits.append(d)
        acc += digits[0] * 10 + digits[-1]

    return acc


if __name__ == "__main__":
    from sys import stdin

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
