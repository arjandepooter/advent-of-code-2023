from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class XY:
    x: int
    y: int

    def __add__(self, other):
        return XY(self.x + other.x, self.y + other.y)


def parse_input(data: str):
    lines = data.splitlines()
    dimensions = (len(lines[0]), len(lines))
    objects = {}

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != ".":
                objects[XY(x, y)] = c

    return objects, dimensions


def find_points(objects, dimensions, start, direction):
    w, h = dimensions
    seen = set()
    queue = [(start, direction)]
    for pos, direction in queue:
        if (
            (pos, direction) in seen
            or pos.x < 0
            or pos.y < 0
            or pos.x >= w
            or pos.y >= h
        ):
            continue
        seen.add((pos, direction))

        match objects.get(pos):
            case "/":
                d = XY(direction.y * -1, direction.x * -1)
                queue.append((pos + d, d))
            case "\\":
                d = XY(direction.y, direction.x)
                queue.append((pos + d, d))
            case "|" if direction.x != 0:
                queue.append((pos + XY(0, 1), XY(0, 1)))
                queue.append((pos + XY(0, -1), XY(0, -1)))
            case "-" if direction.y != 0:
                queue.append((pos + XY(1, 0), XY(1, 0)))
                queue.append((pos + XY(-1, 0), XY(-1, 0)))
            case _:
                queue.append((pos + direction, direction))

    return {pos for pos, _ in seen}


def solve_a(data):
    objects, dimensions = data

    return len(find_points(objects, dimensions, XY(0, 0), XY(1, 0)))


def solve_b(data):
    objects, (w, h) = data

    lengths = []
    for x in range(w):
        lengths.append(len(find_points(objects, (w, h), XY(x, 0), XY(0, 1))))
        lengths.append(len(find_points(objects, (w, h), XY(x, h - 1), XY(0, -1))))
    for y in range(h):
        lengths.append(len(find_points(objects, (w, h), XY(0, y), XY(1, 0))))
        lengths.append(len(find_points(objects, (w, h), XY(w - 1, y), XY(-1, 0))))

    return max(lengths)


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
