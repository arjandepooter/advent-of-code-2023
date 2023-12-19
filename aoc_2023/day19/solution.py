from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    frm: int = 1
    to: int = 4001

    def __len__(self):
        return max(0, self.to - self.frm)

    def __gt__(self, other):
        return Range(max(other + 1, self.frm), self.to)

    def __lt__(self, other):
        return Range(self.frm, min(other, self.to))


@dataclass
class RangeSet:
    x: Range = Range()
    m: Range = Range()
    a: Range = Range()
    s: Range = Range()

    def value(self):
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

    def transform(self, attr, op, threshold):
        new_set = RangeSet(self.x, self.m, self.a, self.s)
        if op == ">":
            setattr(new_set, attr, getattr(new_set, attr) > threshold)
        elif op == "<":
            setattr(new_set, attr, getattr(new_set, attr) < threshold)

        return new_set


def parse_rule(line: str):
    label, rules = line.split("{")
    rules = rules.strip("}").split(",")
    end = rules.pop()
    rules = tuple(tuple(rule.split(":")) for rule in rules)

    return (label, rules, end)


def parse_part(line: str):
    line = line.strip("{}")
    attrs = {}

    for part in line.split(","):
        k, v = part.split("=")
        attrs[k] = int(v)

    return attrs


def parse_input(data: str):
    rules, parts = data.split("\n\n")
    rules = {
        label: (rules, end)
        for label, rules, end in (parse_rule(line) for line in rules.splitlines())
    }
    parts = [parse_part(line) for line in parts.splitlines()]

    return rules, parts


def solve_a(data):
    rules, parts = data
    acc = 0

    for part in parts:
        cur = "in"
        while cur not in ("A", "R"):
            conditions, end = rules[cur]
            for condition, cur in conditions:
                if eval(condition, {}, part):
                    break
            else:
                cur = end
        if cur == "A":
            acc += sum(part.values())

    return acc


def get_combs(rules, ranges=RangeSet(), rule="in"):
    if rule == "A":
        return ranges.value()

    if rule == "R":
        return 0

    acc = 0
    conditions, end = rules[rule]

    for condition, target in conditions:
        op, attr, threshold = (
            (">", *condition.split(">"))
            if ">" in condition
            else ("<", *condition.split("<"))
        )
        threshold = int(threshold)
        acc += get_combs(rules, ranges.transform(attr, op, threshold), target)
        ranges = ranges.transform(
            attr,
            ">" if op == "<" else "<",
            threshold - 1 if op == "<" else threshold + 1,
        )

    return acc + get_combs(rules, ranges, end)


def solve_b(data):
    rules, _ = data

    return get_combs(rules)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
