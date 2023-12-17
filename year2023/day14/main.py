from collections import defaultdict
from functools import cache

from utils.day import AbstractDay


def rotate_counterclockwise(lines: list[str]) -> list[str]:
    return [
        "".join(lines[y][x] for y in range(len(lines)))
        for x in range(len(lines[0]) - 1, -1, -1)
    ]


def rotate_clockwise(lines: list[str]) -> list[str]:
    return [
        "".join(lines[y][x] for y in range(len(lines) - 1, -1, -1))
        for x in range(len(lines[0]))
    ]


@cache
def cached_rotate_and_tilt(all_lines: str) -> str:
    lines = all_lines.split("\n")
    rotated_lines = rotate_clockwise(lines)
    return "\n".join(tilt(rotated_lines))


def tilt(lines: list[str]) -> list[str]:
    tilted_lines = []
    for line in lines:
        splitted_line = line.split("#")
        tilted_line = "#".join("".join(sorted(splitted)) for splitted in splitted_line)
        tilted_lines.append(tilted_line)
    return tilted_lines


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        rotated_lines = rotate_clockwise(lines)
        tilted_lines = tilt(rotated_lines)
        return sum(
            [i for line in tilted_lines for i, c in enumerate(line, 1) if c == "O"]
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        index_of_all_possibilities = defaultdict(list)
        current_lines = "\n".join(lines)
        index_of_all_possibilities[current_lines] = [0]
        total_cycles = 1_000_000_000
        for i in range(total_cycles):
            for j in range(4):  # N, W, S, E
                # we rotate first because we want north to be to the right
                current_lines = cached_rotate_and_tilt(current_lines)

            index_of_all_possibilities[current_lines].append(i + 1)

            if len(index_of_all_possibilities[current_lines]) > 1:
                break

        if i < total_cycles:
            # there is a cycle of cycle
            length = i + 1 - index_of_all_possibilities[current_lines][-2]
            current_mod = (i + 1) % length
            final_mod = total_cycles % length
            while current_mod != final_mod:
                current_mod = (current_mod + 1) % length
                for _ in range(4):  # N, W, S, E
                    current_lines = cached_rotate_and_tilt(current_lines)

        # we still want the load on north and a cycle ends up with East on the right
        lines = rotate_clockwise(current_lines.split("\n"))
        return sum([i for line in lines for i, c in enumerate(line, 1) if c == "O"])
