from itertools import combinations

from utils.day import AbstractDay


def compute_thickness(universe: list[str], expand_thickness: int = 1):
    """
    Return the universe and the thickness of each line and row

    the `expand_thickness` is to expand the universe by adding this number to
    the current thickness of empty row and empty line
    """
    thickness = {"rows": [1 for _ in universe], "cols": [1 for _ in universe[0]]}
    for x in range(len(universe[0])):
        if all(universe[y][x] == "." for y in range(len(universe))):
            thickness["cols"][x] += expand_thickness

    for y in range(len(universe)):
        if all(universe[y][x] == "." for x in range(len(universe[y]))):
            thickness["rows"][y] += expand_thickness

    return thickness


def get_galaxy_positions(universe: list[str]):
    positions = []
    for y in range(len(universe)):
        for x in range(len(universe[y])):
            if universe[y][x] == "#":
                positions.append((x, y))
    return positions


def get_distance(
    thickness: dict[str, list[int]],
    position1: tuple[int, int],
    position2: tuple[int, int],
):
    distance_x = 0
    for x in range(
        position1[0], position2[0], 1 if position1[0] < position2[0] else -1
    ):
        distance_x += thickness["cols"][x]

    distance_y = 0
    for y in range(
        position1[1], position2[1], 1 if position1[1] < position2[1] else -1
    ):
        distance_y += thickness["rows"][y]

    return distance_x + distance_y


class Day(AbstractDay):
    @classmethod
    def _resolve(cls, universe: list[str], expand_thickness: int = 1):
        thickness = compute_thickness(universe, expand_thickness)
        positions = get_galaxy_positions(universe)
        total_length = 0
        for galaxy_position1, galaxy_position2 in combinations(positions, 2):
            total_length += get_distance(thickness, galaxy_position1, galaxy_position2)
        return total_length

    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        return cls._resolve(lines)

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        return cls._resolve(lines, expand_thickness=(1000000 - 1))
