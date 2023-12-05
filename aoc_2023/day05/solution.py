def parse_line(line):
    return line


def split_blocks(data):
    return data.split("\n\n")


def parse_seeds(block):
    lines = block.splitlines()
    assert len(lines) == 1
    _, seeds = lines[0].split(": ")
    seeds = [int(seed) for seed in seeds.split(" ")]

    return seeds


def parse_map(block):
    lines = block.splitlines()
    header, *_ = lines[0].split(" ")
    header = header.split("-")
    frm, to = header[0], header[2]

    ranges = []

    for line in lines[1:]:
        src, dest, length = [int(n) for n in line.split(" ")]
        ranges.append((src, dest, length))

    return (frm, to, ranges)


def parse_input(data):
    blocks = split_blocks(data)
    seeds = parse_seeds(blocks[0])
    maps = {}

    for block in blocks[1:]:
        frm, to, ranges = parse_map(block)
        maps[frm] = (to, ranges)

    return seeds, maps


def solve_a(data):
    seeds, maps = data
    locations = []

    for seed in seeds:
        current = "seed"
        while current != "location":
            current, ranges = maps[current]

            for dest, frm, length in ranges:
                if frm <= seed <= frm + length:
                    seed += dest - frm
                    break
        locations.append(seed)

    return min(locations)


def find_overlap(range1, range2):
    """
    >>> find_overlap((79, 10), (70, 10))
    (None, (79, 1), (80, 9))

    >>> find_overlap((78, 10), (80, 10))
    ((78, 2), (80, 8), None)

    >>> find_overlap((79, 10), (100, 10))
    ((79, 10), None, None)

    >>> find_overlap((79, 10), (70, 20))
    (None, (79, 10), None)

    >>> find_overlap((79, 10), (40, 5))
    (None, None, (79, 10))

    >>> find_overlap((70, 20), (79, 10))
    ((70, 9), (79, 10), (89, 1))
    """
    start1, length1 = range1
    start2, length2 = range2

    head = overlap = tail = None

    if start1 < start2:
        head = (start1, min(start2 - start1, length1))
    if start1 + length1 > start2 + length2:
        tail = (
            s := max(start2 + length2, start1),
            length1 - (s - start1),
        )
    if start1 <= start2 < start1 + length1:
        overlap = (start2, min(start1 + length1 - start2, length2))
    if start2 <= start1 < start2 + length2:
        overlap = (start1, min(start2 + length2 - start1, length1))

    return head, overlap, tail


def solve_b(data):
    seeds, maps = data
    source_ranges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    current = "seed"

    while current != "location":
        current, ranges = maps[current]
        new_ranges = []

        for source_start, source_length in source_ranges:
            for dest, frm, length in ranges:
                head, overlap, tail = find_overlap(
                    (source_start, source_length),
                    (frm, length),
                )

                if overlap:
                    new_ranges.append((overlap[0] + dest - frm, overlap[1]))
                    if head:
                        source_ranges.append(head)
                    if tail:
                        source_ranges.append(tail)
                    break
            else:
                new_ranges.append((source_start, source_length))

        source_ranges = new_ranges

    return min(source_ranges, key=lambda x: x[0])[0]


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
