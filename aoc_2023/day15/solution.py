from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Lens:
    label: str
    f: int = field(hash=False, compare=False, default=-1)

    @classmethod
    def from_str(cls, s):
        if s.endswith("-"):
            return cls(s[:-1])
        else:
            return cls(s[:-2], int(s[-1]))


def parse_input(data: str):
    return data.split(",")


def hash(s):
    acc = 0
    for c in s:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def solve_a(data):
    return sum(hash(s) for s in data)


def solve_b(data):
    boxes = defaultdict(list)
    lenses = [Lens.from_str(s) for s in data]

    for lens in lenses:
        box = boxes[hash(lens.label)]

        match (lens.f, lens in box):
            case -1, True:
                box.remove(lens)
            case -1, False:
                ...
            case _, True:
                box[box.index(lens)] = lens
            case _, False:
                box.append(lens)

    acc = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses, 1):
            acc += (box + 1) * i * lens.f
    return acc


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
