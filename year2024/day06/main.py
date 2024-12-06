from utils.day import AbstractDay
from utils.grid2D import Directions, Grid, Position

OBSTACLE = "#"


class InLoopError(Exception):
    pass


def turn_right(current_direction: Directions) -> Directions:
    return {
        Directions.RIGHT: Directions.DOWN,
        Directions.UP: Directions.RIGHT,
        Directions.LEFT: Directions.UP,
        Directions.DOWN: Directions.LEFT,
    }[current_direction]


def get_start_position(lines: list[str]) -> Position:
    return Position(
        *[
            (x, y)
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
            if char != OBSTACLE and char != "."
        ][0]
    )


def get_seens(lines: list[str]) -> set[Position]:
    grid = Grid(lines)
    position = get_start_position(lines)
    current_direction = {
        "^": Directions.UP,
        "v": Directions.DOWN,
        ">": Directions.RIGHT,
        "<": Directions.LEFT,
    }[grid.get_from_position(position)]

    seen_with_direction: set[tuple[Position, Directions]] = set()
    while True:
        if (position, current_direction) in seen_with_direction:
            raise InLoopError()
        seen_with_direction.add((position, current_direction))
        next_position = position.move(current_direction)
        first_direction = current_direction
        while (
            grid.is_inside(next_position)
            and grid.get_from_position(next_position) == OBSTACLE
        ):
            current_direction = turn_right(current_direction)
            next_position = position.move(current_direction)
            if current_direction == first_direction:
                raise InLoopError()

        if not grid.is_inside(next_position):
            seen, *_ = zip(*seen_with_direction)
            return set(seen)

        position = next_position


class Day(AbstractDay):

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        return len(get_seens(lines))

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        start_position = get_start_position(lines)
        seen = get_seens(lines)
        count_loops = 0
        for position in seen:
            if position == start_position:
                continue
            new_lines = lines.copy()
            new_lines[position.y] = (
                new_lines[position.y][: position.x]
                + OBSTACLE
                + new_lines[position.y][position.x + 1 :]
            )
            try:
                get_seens(new_lines)
            except InLoopError:
                count_loops += 1
        return count_loops
