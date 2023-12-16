from collections.abc import Iterator
from enum import Enum
from itertools import product


class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def iter_around(self, include_diagonales=True) -> Iterator["Position"]:
        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if dx == dy == 0 or (not include_diagonales and dx * dy != 0):
                continue
            yield Position(self.x + dx, self.y + dy)

    def move(self, direction: Directions) -> "Position":
        return Position(self.x + direction.value[0], self.y + direction.value[1])

    def __eq__(self, other: "Position") -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Position ({self.x}, {self.y})"


class Grid:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def is_inside(self, position: Position) -> bool:
        return 0 <= position.y < len(self.lines) and 0 <= position.x < len(
            self.lines[position.y]
        )

    def get_from_position(self, position: Position) -> str | None:
        return self.lines[position.y][position.x] if self.is_inside(position) else None
