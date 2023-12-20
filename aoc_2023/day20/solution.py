from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from math import lcm
from typing import Self


class Type(StrEnum):
    BROADCAST = ""
    FLIPFLOP = "%"
    CONJUNCTION = "&"
    VOID = "y"


@dataclass
class Node:
    label: str
    inputs: list[Self]
    outputs: list[Self]
    type: Type
    value: bool = False

    def emit(self, other):
        if not hasattr(self, "_pulses"):
            self._pulses = defaultdict(int)

        self._pulses[self.value] += 1

        return self >> other

    def pulses(self, v):
        if hasattr(self, "_pulses"):
            return self._pulses[v]
        return 0

    def __rshift__(other, self):
        match self.type:
            case Type.BROADCAST:
                self.value = other.value
                return True
            case Type.FLIPFLOP:
                self.value = not (self.value ^ other.value)
                return not other.value
            case Type.CONJUNCTION:
                if not hasattr(self, "_memory"):
                    self._memory = {input.label: False for input in self.inputs}
                self._memory[other.label] = other.value
                self.value = any(not pulse for pulse in self._memory.values())
                return True
            case Type.VOID:
                if other.value:
                    self.value = True
                return False


def parse_input(data: str):
    nodes = {
        "button": (Node("button", [], [], Type.BROADCAST), ["broadcaster"]),
    }

    for line in data.splitlines():
        t, children = line.split(" -> ")
        typ = Type("" if t[0].isalpha() else t[0])
        label = t.lstrip("%&")
        children = children.split(", ")
        node = Node(label, [], [], typ)
        nodes[node.label] = (node, children)

    for node, children in list(nodes.values()):
        for child in children:
            child_node = Node(child, [], [], Type.VOID)
            if child in nodes:
                child_node, _ = nodes[child]
            else:
                nodes[child] = (child_node, [])
            node.outputs.append(child_node)
            child_node.inputs.append(node)

    return {node.label: node for node, _ in nodes.values()}


def solve_a(nodes):
    nodes = parse_input(data)

    for _ in range(1000):
        queue = [nodes["button"]]

        for node in queue:
            for output in node.outputs:
                if node.emit(output):
                    queue.append(output)

    return sum(node.pulses(False) for node in nodes.values()) * sum(
        node.pulses(True) for node in nodes.values()
    )


def solve_b(data):
    nodes = parse_input(data)
    targets = [t.label for t in nodes["rx"].inputs[0].inputs]
    periods = {}

    n = 0
    while len(list(periods.values())) < len(targets):
        queue = [nodes["button"]]
        n += 1

        for node in queue:
            if node.label in targets and node.value and node.label not in periods:
                periods[node.label] = n
            for output in node.outputs:
                if node.emit(output):
                    queue.append(output)

    return lcm(*periods.values())


if __name__ == "__main__":
    from doctest import testmod
    from sys import stdin

    testmod()

    data = stdin.read()
    print(solve_a(data))
    print(solve_b(data))
