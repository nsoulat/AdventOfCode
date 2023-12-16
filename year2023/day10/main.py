from collections.abc import Iterator

from utils.class_helper import WithID
from utils.day import AbstractDay
from utils.grid2D import Directions, Position

DIRECTIONS_PER_TILE: dict[str, tuple[Directions, Directions]] = {
    # directions are ordered -> LEFT < UP < DOWN < RIGHT
    "|": (Directions.UP, Directions.DOWN),
    "-": (Directions.LEFT, Directions.RIGHT),
    "L": (Directions.UP, Directions.RIGHT),
    "J": (Directions.LEFT, Directions.UP),
    "7": (Directions.LEFT, Directions.DOWN),
    "F": (Directions.DOWN, Directions.RIGHT),
}


def guess_pipe_type(
    up_type: str | None,
    right_type: str | None,
    down_type: str | None,
    left_type: str | None,
) -> str:
    directions = []
    if Directions.RIGHT in DIRECTIONS_PER_TILE.get(left_type, []):
        directions.append(Directions.LEFT)
    if Directions.DOWN in DIRECTIONS_PER_TILE.get(up_type, []):
        directions.append(Directions.UP)
    if Directions.UP in DIRECTIONS_PER_TILE.get(down_type, []):
        directions.append(Directions.DOWN)
    if Directions.LEFT in DIRECTIONS_PER_TILE.get(right_type, []):
        directions.append(Directions.RIGHT)
    directions = tuple(directions)
    for pipe_type, tile_directions in DIRECTIONS_PER_TILE.items():
        if tile_directions == directions:
            return pipe_type
    print("Not found", directions, (up_type, right_type, down_type, left_type))
    return "."


class Tile(WithID):
    def __init__(self, pipe_type: str, position: Position):
        super().__init__()
        self.pipe_type = pipe_type
        self.position = position

    def iter_around(self) -> Iterator[tuple["Position", Directions]]:
        for direction in DIRECTIONS_PER_TILE[self.pipe_type]:
            yield (
                Position(
                    self.position.x + direction.value[0],
                    self.position.y + direction.value[1],
                ),
                direction,
            )

    def next_position_and_direction(
        self, previous_position: Position
    ) -> tuple[Position, Directions]:
        # there is only two positions in iter_around
        for position, direction in self.iter_around():
            if position != previous_position:
                return (position, direction)


class Grid:
    def __init__(self, lines: list[str]):
        self.tiles_by_position: dict[Position, Tile] = {}
        for y, line in enumerate(lines):
            for x, pipe_type in enumerate(line):
                if pipe_type == "S":
                    self.start_position = Position(x, y)
                    pipe_type = self._guess_tile_type(lines, self.start_position)
                if pipe_type != ".":
                    position = Position(x, y)
                    self.tiles_by_position[position] = Tile(
                        pipe_type=pipe_type, position=position
                    )

    def get_tile(self, position: Position) -> Tile | None:
        return self.tiles_by_position.get(position)

    def get_start_tile(self) -> Tile:
        return self.tiles_by_position[self.start_position]

    def _guess_tile_type(self, lines: list[str], position: Position) -> str:
        def get_if_inside(x: int, y: int) -> str | None:
            if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
                return lines[y][x]

        x, y = position.x, position.y
        return guess_pipe_type(
            up_type=get_if_inside(x, y - 1),
            right_type=get_if_inside(x + 1, y),
            down_type=get_if_inside(x, y + 1),
            left_type=get_if_inside(x - 1, y),
        )


def get_loop(grid: Grid) -> list[Tile]:
    start = grid.get_start_tile()
    start_position = start.position
    current_position, direction = start.next_position_and_direction(
        start_position  # hack to take the first next position
    )
    previous_position = start_position
    loop = [start]
    while current_position != start_position:
        current_tile = grid.get_tile(current_position)
        (
            previous_position,
            (current_position, _),
        ) = current_position, current_tile.next_position_and_direction(
            previous_position=previous_position
        )
        loop.append(current_tile)
    return loop


def compute_area(lines: list[str], loop: list[Tile]) -> int:
    loop_positions = {tile.position for tile in loop}
    count = 0
    in_area = False  # we begin ouside
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if Position(x, y) in loop_positions:
                if lines[y][x] in "|LJ":
                    # the parity change, we enter/exit the inside of the loop
                    in_area = not in_area
            else:
                count += 1 if in_area else 0
    return count


class Day(AbstractDay):
    @classmethod
    def _resolve_part1(cls, lines: list[str]):
        grid = Grid(lines=lines)
        loop = get_loop(grid)
        # we have visited all the loop, the farthest point is the length divided by 2
        return len(loop) // 2

    @classmethod
    def _resolve_part2(cls, lines: list[str]):
        grid = Grid(lines=lines)
        loop = get_loop(grid)
        return compute_area(lines, loop)
