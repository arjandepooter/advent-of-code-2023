from collections import defaultdict
from random import choice
from dataclasses import dataclass
from copy import deepcopy
from collections import Counter


class Edge:
    def __init__(self, frm, to):
        self.frm, self.to = tuple(sorted([frm, to]))

    def __eq__(self, other):
        return (self.frm, self.to) == (other.frm, other.to)

    def __hash__(self):
        return hash((self.frm, self.to))


def parse_input(data: str):
    nodes = set()
    edges = set()

    for line in data.splitlines():
        frm, tos = line.split(": ")
        for to in tos.split(" "):
            nodes.add(frm)
            nodes.add(to)
            edges.add(Edge(frm, to))

    return nodes, edges


def karger(orig_nodes, orig_edges):
    edges = deepcopy(orig_edges)
    nodes = deepcopy(orig_nodes)
    sets = {n: [n] for n in nodes}

    while len(nodes) > 2:
        edge_to_cut = choice(list(edges))
        node = edge_to_cut.to
        nodes.remove(node)
        sets[edge_to_cut.frm] += sets[node]
        del sets[node]

        for edge in list(edges):
            if edge.frm != node and edge.to != node:
                continue
            edges.remove(edge)

            d = edge.to if edge.frm == node else edge.frm
            if d != edge_to_cut.frm:
                edges.add(Edge(d, edge_to_cut.frm))

    sets = list(sets.values())
    set1 = set(sets[0])
    set2 = set(sets[1])

    cuts = 0
    for edge in orig_edges:
        if edge.frm in set1 and edge.to in set2:
            cuts += 1
        if edge.to in set1 and edge.frm in set2:
            cuts += 1

    return cuts, len(set1) * len(set2)


def solve_a(data):
    while True:
        cuts, result = karger(*data)
        if cuts == 3:
            return result


def solve_b(data):
    pass


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = parse_input(stdin.read().strip())
    print(solve_a(data))
    print(solve_b(data))
