from collections.abc import Iterator
from enum import Enum
from itertools import product


class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    def __repr__(self):
        return str(self)


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def iter_around(self, include_diagonales=True) -> Iterator["Position"]:
        for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
            if dx == dy == 0 or (not include_diagonales and dx * dy != 0):
                continue
            yield Position(self.x + dx, self.y + dy)

    def move(self, direction: Directions, length: int = 1) -> "Position":
        return Position(
            self.x + length * direction.value[0],
            self.y + length * direction.value[1],
        )

    def __eq__(self, other: "Position") -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Position ({self.x}, {self.y})"

    def __add__(self, other) -> "Position":
        if isinstance(other, Position):
            return Position(self.x + other.x, self.y + other.y)
        if isinstance(other, tuple) and len(other) == 2:
            return Position(self.x + other[0], self.y + other[1])
        return NotImplemented

    def __sub__(self, other) -> tuple[int, int]:
        if isinstance(other, Position):
            return (self.x - other.x, self.y - other.y)
        if isinstance(other, tuple) and len(other) == 2:
            return (self.x - other[0], self.y - other[1])
        return NotImplemented


class Grid:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def is_inside(self, position: Position) -> bool:
        return 0 <= position.y < len(self.lines) and 0 <= position.x < len(
            self.lines[position.y]
        )

    def get_from_position(self, position: Position) -> str | None:
        return self.lines[position.y][position.x] if self.is_inside(position) else None


def scalar_product(x1, y1, x2, y2) -> int:
    return x1 * x2 + y1 * y2
