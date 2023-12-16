from collections import defaultdict

from utils.day import AbstractDay
from utils.grid2D import Directions, Grid, Position


def get_new_directions(
    grid: Grid, current_position: Position, previous_direction: Directions
) -> list[Directions]:
    if not (tile := grid.get_from_position(current_position)):
        return []

    if (
        tile == "."
        or (tile == "|" and previous_direction in {Directions.UP, Directions.DOWN})
        or (tile == "-" and previous_direction in {Directions.LEFT, Directions.RIGHT})
    ):
        return [previous_direction]

    next_mirror_direction = {
        "/": {
            Directions.UP: Directions.RIGHT,
            Directions.DOWN: Directions.LEFT,
            Directions.LEFT: Directions.DOWN,
            Directions.RIGHT: Directions.UP,
        },
        "\\": {
            Directions.UP: Directions.LEFT,
            Directions.DOWN: Directions.RIGHT,
            Directions.LEFT: Directions.UP,
            Directions.RIGHT: Directions.DOWN,
        },
    }

    if tile in next_mirror_direction:
        new_direction = next_mirror_direction[tile][previous_direction]
        return [new_direction]

    if tile == "|":
        # previous_direction is either LEFT or RIGHT
        return [Directions.UP, Directions.DOWN]
    if tile == "-":
        # previous_direction is either UP or DOWN
        return [Directions.LEFT, Directions.RIGHT]

    return []


def energized(
    grid: Grid,
    start: Position = Position(0, 0),
    direction: Directions = Directions.RIGHT,
) -> dict[Position, set[Directions]]:
    # remember for each tile position from which directions it has been energized
    energized: dict[Position, set[Directions]] = defaultdict(set)

    energized[start].add(direction)
    to_move = [(start, direction)]

    while to_move:
        next_to_move = []
        for current_position, previous_direction in to_move:
            new_directions = get_new_directions(
                grid=grid,
                current_position=current_position,
                previous_direction=previous_direction,
            )
            for new_direction in new_directions:
                new_position = current_position.move(new_direction)
                if not grid.is_inside(new_position):
                    continue
                if new_direction not in energized[new_position]:
                    energized[new_position].add(new_direction)
                    next_to_move.append((new_position, new_direction))
        to_move = next_to_move

    return energized


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        grid = Grid(lines)
        energized_grid = energized(grid)
        return len(energized_grid.keys())

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        max_energized = 0
        grid = Grid(lines)
        starts_with_direction = [
            *[(Position(x, 0), Directions.DOWN) for x in range(len(grid.lines[0]))],
            *[
                (Position(x, len(grid.lines) - 1), Directions.UP)
                for x in range(len(grid.lines[0]))
            ],
            *[(Position(0, y), Directions.LEFT) for y in range(len(grid.lines))],
            *[
                (Position(len(grid.lines[0]) - 1, y), Directions.RIGHT)
                for y in range(len(grid.lines))
            ],
        ]
        for start, direction in starts_with_direction:
            max_energized = max(
                max_energized,
                len(energized(grid=grid, start=start, direction=direction).keys()),
            )
        return max_energized
