from collections import defaultdict
from itertools import product

from utils.day import AbstractDay
from utils.grid2D import Grid, Position


def get_all_antinodes(
    grid: Grid, antennas_by_frequency: dict[str, set[Position]], only_first: bool
) -> set[Position]:
    seen_antinodes = set()
    for antennas in antennas_by_frequency.values():
        for antenna1, antenna2 in product(antennas, antennas):
            if antenna1 == antenna2:
                continue
            diff = antenna1 - antenna2
            possible_antinode = antenna1
            while grid.is_inside((possible_antinode := possible_antinode + diff)):
                seen_antinodes.add(possible_antinode)
                if only_first:
                    break

    return seen_antinodes


def get_antennas_by_frequency(lines: list[str]) -> dict[str, set[Position]]:
    antennas_by_frequency: dict[str, set[Position]] = defaultdict(set)
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == ".":
                continue
            antennas_by_frequency[character].add(Position(x, y))
    return antennas_by_frequency


class Day(AbstractDay):

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        antennas_by_frequency = get_antennas_by_frequency(lines)
        grid = Grid(lines)
        return len(
            get_all_antinodes(
                grid=grid, antennas_by_frequency=antennas_by_frequency, only_first=True
            )
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        antennas_by_frequency = get_antennas_by_frequency(lines)
        return len(
            {
                *get_all_antinodes(
                    grid=Grid(lines),
                    antennas_by_frequency=antennas_by_frequency,
                    only_first=False,
                ),
                *(  # ensure that all antennas that are not unique in frequency
                    # are always taking into account
                    antenna
                    for antennas in antennas_by_frequency.values()
                    if len(antennas) > 1
                    for antenna in antennas
                ),
            }
        )
