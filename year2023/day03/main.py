from collections import defaultdict

from utils.class_helper import WithID
from utils.day import AbstractDay
from utils.grid2D import Grid as BaseGrid
from utils.grid2D import Position

EXCLUDED_SYMBOLS = {"."}


class Symbol:
    pass


class PartNumber(WithID):
    def __init__(self, number: int):
        super().__init__()
        self.number = number
        self.adj_symbols: set[Symbol] = set()

    def __mul__(self, other: "PartNumber") -> int:
        return self.number * other.number


class Grid(BaseGrid):
    def __init__(self, lines: list[str]):
        super().__init__(lines=lines)
        self.part_numbers: list[PartNumber] = []


def is_digit(grid: Grid, position: Position) -> bool:
    """Return True only if there is a digit at the position"""
    character = grid.get_from_position(position)
    return False if character is None else character.isdigit()


def get_number_by_position(grid: Grid) -> dict[Position, PartNumber]:
    """
    Create a dict that for each (x,y) position ((0,0) is top left)
     returns the PartNumber of this position if it exists (meaning one of the digit
     is at (x,y))
    """
    number_by_position = {}
    tmp_value = 0
    # the PartNumber will be added to all these positions
    positions_to_add: list[Position] = []

    for y, line in enumerate(grid.lines):
        for x, character in enumerate(line):
            pos = Position(x, y)
            if character.isdigit():
                positions_to_add.append(pos)
                tmp_value = (10 * tmp_value) + int(character)
                if not is_digit(grid, Position(x + 1, y)):
                    # If next character is not a digit, we create
                    #  the PartNumber
                    part_number = PartNumber(tmp_value)
                    grid.part_numbers.append(part_number)
                    for position in positions_to_add:
                        number_by_position[position] = part_number
                    tmp_value, positions_to_add = 0, []

    return number_by_position


class Day(AbstractDay):
    @classmethod
    def resolve_part1(cls, lines: list[str]):
        grid = Grid(lines)
        number_by_position = get_number_by_position(grid)
        for y, line in enumerate(grid.lines):
            for x, character in enumerate(line):
                pos = Position(x, y)
                if not character.isdigit() and character not in EXCLUDED_SYMBOLS:
                    symbol_obj = Symbol()
                    for pos_around in pos.iter_around():
                        if part_number := number_by_position.get(pos_around):
                            part_number.adj_symbols.add(symbol_obj)

        return sum(
            part_number.number
            for part_number in grid.part_numbers
            if part_number.adj_symbols
        )

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        grid = Grid(lines)
        number_by_position = get_number_by_position(grid)
        adj_parts_by_symbols = defaultdict(set)
        for y, line in enumerate(grid.lines):
            for x, character in enumerate(line):
                pos = Position(x, y)
                if not character.isdigit() and character not in EXCLUDED_SYMBOLS:
                    symbol_obj = Symbol()
                    for pos_around in pos.iter_around():
                        if part_number := number_by_position.get(pos_around):
                            part_number.adj_symbols.add(symbol_obj)
                            if character == "*":
                                adj_parts_by_symbols[symbol_obj].add(part_number)

        gear_ratios = [
            part_numbers
            for _, part_numbers in adj_parts_by_symbols.items()
            if len(part_numbers) == 2
        ]
        return sum(
            part_number1 * part_number2 for (part_number1, part_number2) in gear_ratios
        )
