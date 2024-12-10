from utils.day import AbstractDay
from utils.grid2D import Grid, Position


def get_scores(grid: Grid, position: Position) -> tuple[int, int]:
    """Return the number of ending trails position and the number of distinct trails"""
    end_of_trails: list[Position] = []

    def move_until_nine(height: int, current_position: Position):
        if height == 9:
            end_of_trails.append(current_position)
            return
        for next_position in current_position.iter_around(include_diagonales=False):
            if int(grid.get_from_position(next_position) or -1) == height + 1:
                move_until_nine(height + 1, next_position)

    move_until_nine(0, position)
    return len(set(end_of_trails)), len(end_of_trails)


class Day(AbstractDay):

    @classmethod
    def resolve_part1(cls, lines: list[str]):
        grid = Grid(lines)
        scores_sum = 0
        for y, line in enumerate(grid.lines):
            for x, height in enumerate(line):
                if int(height) == 0:
                    scores_sum += get_scores(grid, Position(x, y))[0]
        return scores_sum

    @classmethod
    def resolve_part2(cls, lines: list[str]):
        grid = Grid(lines)
        scores_sum = 0
        for y, line in enumerate(grid.lines):
            for x, height in enumerate(line):
                if int(height) == 0:
                    scores_sum += get_scores(grid, Position(x, y))[1]
        return scores_sum
