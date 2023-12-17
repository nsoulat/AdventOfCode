import math
from typing import Callable

from utils.day import AbstractDay
from utils.file import get_sections

MAX_COUNT = 1000000


def follow_instructions(
    instructions: list[str],
    graph: dict[str, tuple[str, str]],
    starts: list[str],
    ending_fun: Callable[..., bool],
) -> int:
    count = 0
    current_locations = starts.copy()
    while not ending_fun(current_locations):
        next_locations = []
        for current in current_locations:
            left, right = graph[current]
            instruction = instructions[count % len(instructions)]
            next_locations.append(left if instruction == "L" else right)
        current_locations = next_locations
        count += 1
        if count > MAX_COUNT:
            raise Exception("Too much steps: ", count)
    return count


def follow_instructions_v2(
    instructions: list[str],
    graph: dict[str, tuple[str, str]],
    starts: list[str],
    endings: set[str],
) -> int:
    first_ending_per_start = {}
    for start in starts.copy():
        count = 0
        current = start
        while current not in endings or count > MAX_COUNT:
            left, right = graph[current]
            instruction = instructions[count % len(instructions)]
            current = left if instruction == "L" else right
            count += 1
        if count > MAX_COUNT:
            raise Exception("Too much steps: ", count)
        first_ending_per_start[start] = count
    return math.lcm(*first_ending_per_start.values())


def get_instructions(section: list[str]) -> list[str]:
    return [*section[0]]


def get_graph(section: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    graph = {}
    for line in section:
        node, destinations = line.split(" = ")
        left, right = destinations[1:-1].split(", ")  # remove parenthesis and split
        graph[node] = (left, right)
    return graph


def get_instructions_and_graph(
    lines: list[str],
) -> tuple[list[str], dict[str, tuple[str, str]]]:
    (instruction_section, graph_section) = get_sections(lines)
    instructions = get_instructions(instruction_section)
    graph = get_graph(graph_section)
    return instructions, graph


def end_when_reached_ZZZ(locations: list[str]) -> bool:
    return locations == ["ZZZ"]


def end_when_all_end_with_Z(locations: list[str]) -> bool:
    return all(location.endswith("Z") for location in locations)


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        instructions, graph = get_instructions_and_graph(lines)
        return follow_instructions(
            instructions, graph, starts=["AAA"], ending_fun=end_when_reached_ZZZ
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        instructions, graph = get_instructions_and_graph(lines)
        return follow_instructions_v2(
            instructions,
            graph,
            starts=[loc for loc in graph.keys() if loc.endswith("A")],
            endings={loc for loc in graph.keys() if loc.endswith("Z")},
        )
